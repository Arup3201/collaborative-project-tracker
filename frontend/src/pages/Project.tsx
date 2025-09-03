import React, { useState, useMemo, useEffect } from "react";
import { useParams } from "react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Plus,
  Edit,
  Trash2,
  Eye,
  UserPlus,
  User,
  Clock,
  CheckCircle2,
  Circle,
  MoreHorizontal,
  Loader2,
} from "lucide-react";

import { HttpGet, HttpPost } from "@/utils/http";

import type { Project as ProjectType } from "@/types/project";
import type { Task, TeamMember, NewTaskData, TaskStatus } from "@/types/task";
import type { MemberResponse, TaskResponse } from "@/types/response";

const Project: React.FC = () => {
  const { id: project_id } = useParams();

  const [isLoading, setIsLoading] = useState(false);

  const [project, setProject] = useState<ProjectType>({} as ProjectType);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);

  const getProject = async (projectId: string) => {
    setIsLoading(true);
    try {
      const data = await HttpGet(`/projects/${projectId}`);
      setProject({
        ...data.project,
      });
      setTasks(() => data.tasks.map((task: TaskResponse) => ({
        id: task.id, 
        name: task.name, 
        description: task.description, 
        status: task.status, 
        assignee: {
          id: task.assignee, 
          name: task.assignee_name, 
          email: task.assignee_email
        }
      })));
    } catch (err) {
      console.error(`getProject failed: ${err}`);
    } finally {
      setIsLoading(false);
    }
  };
  const getMembers = async (projectId: string) => {
    try {
      const data = await HttpGet(`/projects/${projectId}/members`);
      setTeamMembers(() =>
        data.members.map((member: MemberResponse) => ({
          id: member.user_id,
          email: member.email,
          name: member.name,
          joinedAt: member.joined_at,
          role: member.role,
        }))
      );
    } catch (err) {
      console.error(`getMembers failed: ${err}`);
    }
  };
  useEffect(() => {
    if (project_id) {
      getProject(project_id);
      getMembers(project_id);
    }
  }, [project_id]);

  const [newTask, setNewTask] = useState<NewTaskData>({
    name: "",
    description: "",
    assignee: "",
    status: "To Do",
  });

  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [createError, setCreateError] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState<{
    [key: string]: boolean;
  }>({});

  const toggleDropdown = (taskId: string) => {
    setIsDropdownOpen((prev) => ({
      ...prev,
      [taskId]: !prev[taskId],
    }));
  };

  const handleCreateTask = async () => {
    setCreateError("");

    if (
      !newTask.name.trim() ||
      !newTask.description.trim() ||
      !newTask.assignee
    ) {
      setCreateError("All fields are required");
      return;
    }

    setIsCreating(true);

    try {
      const data = await HttpPost(`/projects/${project_id}/tasks/`, {
        name: newTask.name,
        description: newTask.description,
        assignee: newTask.assignee,
        status: newTask.status,
      });

      console.log("Creating task:", newTask);

      setTasks((prev) => [
        ...prev,
        {
          id: data.task.id,
          name: data.task.name,
          description: data.task.description,
          assignee: {
            id: data.task.assignee,
            name: data.task.assignee_name,
            email: data.task.assignee_email,
          },
          status: data.task.status,
        },
      ]);

      // Reset form and close dialog
      setNewTask({
        name: "",
        description: "",
        assignee: "",
        status: "To Do",
      });
      setIsCreateDialogOpen(false);
    } catch (err) {
      setCreateError("Failed to create task. Please try again.");
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      // TODO: Replace with your actual delete task API call
      console.log("Deleting task:", taskId);
      setTasks((prev) => prev.filter((task) => task.id !== taskId));
    } catch (err) {
      console.error("Failed to delete task");
    }
  };

  const handleEditTask = (taskId: string) => {
    // TODO: Implement edit task functionality
    console.log("Edit task:", taskId);
  };

  const handleViewTask = (taskId: string) => {
    // TODO: Implement view task details functionality
    console.log("View task:", taskId);
  };

  const handleAssignTask = (taskId: string) => {
    // TODO: Implement assign task functionality
    console.log("Assign task:", taskId);
  };

  const truncateDescription = (description: string, maxLength: number = 50) => {
    return description.length > maxLength
      ? description.substring(0, maxLength) + "..."
      : description;
  };

  const getStatusBadge = (status: TaskStatus) => {
    const statusConfig: any = {
      "To Do": {
        color: "bg-gray-100 text-gray-800",
        icon: <Circle className="w-3 h-3" />,
      },
      "In Progress": {
        color: "bg-blue-100 text-blue-800",
        icon: <Clock className="w-3 h-3" />,
      },
      Done: {
        color: "bg-green-100 text-green-800",
        icon: <CheckCircle2 className="w-3 h-3" />,
      },
    };

    const config = statusConfig[status];

    return (
      <Badge className={`${config.color} flex items-center gap-1`}>
        {config.icon}
        {status}
      </Badge>
    );
  };

  // TanStack Table setup
  const columnHelper = createColumnHelper<Task>();

  const columns = useMemo(
    () => [
      columnHelper.accessor("name", {
        header: "Task Name",
        cell: (info) => <div className="font-medium">{info.getValue()}</div>,
      }),
      columnHelper.accessor("description", {
        header: "Description",
        cell: (info) => (
          <span className="text-stone-600" title={info.getValue()}>
            {truncateDescription(info.getValue())}
          </span>
        ),
      }),
      columnHelper.accessor("assignee", {
        header: "Assignee",
        cell: (info) => (
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-stone-400" />
            {info.getValue().name}
          </div>
        ),
      }),
      columnHelper.accessor("status", {
        header: "Status",
        cell: (info) => getStatusBadge(info.getValue()),
      }),
      columnHelper.display({
        id: "actions",
        header: "Actions",
        cell: (info) => (
          <div className="relative text-right">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleDropdown(info.row.original.id)}
            >
              <MoreHorizontal className="w-4 h-4" />
            </Button>

            {isDropdownOpen[info.row.original.id] && (
              <div className="top-full right-0 z-50 absolute bg-white shadow-lg mt-1 border border-stone-200 rounded-md min-w-32">
                <div
                  onClick={() => {
                    handleViewTask(info.row.original.id);
                    setIsDropdownOpen((prev) => ({
                      ...prev,
                      [info.row.original.id]: false,
                    }));
                  }}
                  className="flex items-center hover:bg-stone-100 px-2 py-2 text-sm cursor-pointer"
                >
                  <Eye className="mr-2 w-4 h-4" />
                  View Task
                </div>
                <div
                  onClick={() => {
                    handleEditTask(info.row.original.id);
                    setIsDropdownOpen((prev) => ({
                      ...prev,
                      [info.row.original.id]: false,
                    }));
                  }}
                  className="flex items-center hover:bg-stone-100 px-2 py-2 text-sm cursor-pointer"
                >
                  <Edit className="mr-2 w-4 h-4" />
                  Edit
                </div>
                <div
                  onClick={() => {
                    handleAssignTask(info.row.original.id);
                    setIsDropdownOpen((prev) => ({
                      ...prev,
                      [info.row.original.id]: false,
                    }));
                  }}
                  className="flex items-center hover:bg-stone-100 px-2 py-2 text-sm cursor-pointer"
                >
                  <UserPlus className="mr-2 w-4 h-4" />
                  Assign
                </div>
                <div
                  onClick={() => {
                    handleDeleteTask(info.row.original.id);
                    setIsDropdownOpen((prev) => ({
                      ...prev,
                      [info.row.original.id]: false,
                    }));
                  }}
                  className="flex items-center hover:bg-stone-100 px-2 py-2 text-red-600 text-sm cursor-pointer"
                >
                  <Trash2 className="mr-2 w-4 h-4" />
                  Delete
                </div>
              </div>
            )}
          </div>
        ),
      }),
    ],
    [isDropdownOpen]
  );

  const table = useReactTable({
    data: tasks,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="bg-stone-50 p-6 min-h-screen">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="mb-2 font-bold text-stone-900 text-3xl">
            {project.name}
          </h1>
          <p className="text-stone-600">Manage tasks and track progress</p>
        </div>

        {/* Tasks Table */}
        <Card>
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-xl">Tasks</CardTitle>

            {/* Create New Task Button - moved to the right */}
            <Dialog
              open={isCreateDialogOpen}
              onOpenChange={setIsCreateDialogOpen}
            >
              <DialogTrigger asChild>
                <Button className="flex items-center gap-2">
                  <Plus className="w-4 h-4" />
                  Create New Task
                </Button>
              </DialogTrigger>

              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle>Create New Task</DialogTitle>
                  <DialogDescription>
                    Fill in the details below to create a new task
                  </DialogDescription>
                </DialogHeader>

                <div className="space-y-4">
                  {createError && (
                    <Alert variant="destructive">
                      <AlertDescription>{createError}</AlertDescription>
                    </Alert>
                  )}

                  <div className="space-y-2">
                    <Label htmlFor="taskName">Task Name</Label>
                    <Input
                      id="taskName"
                      placeholder="Enter task name"
                      value={newTask.name}
                      onChange={(e) =>
                        setNewTask((prev) => ({
                          ...prev,
                          name: e.target.value,
                        }))
                      }
                      disabled={isCreating}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="taskDescription">Description</Label>
                    <Textarea
                      id="taskDescription"
                      placeholder="Enter task description"
                      value={newTask.description}
                      onChange={(e) =>
                        setNewTask((prev) => ({
                          ...prev,
                          description: e.target.value,
                        }))
                      }
                      disabled={isCreating}
                      rows={3}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="taskAssignee">Assignee</Label>
                    <Select
                      value={newTask.assignee}
                      onValueChange={(value) =>
                        setNewTask((prev) => ({ ...prev, assignee: value }))
                      }
                      disabled={isCreating}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select assignee" />
                      </SelectTrigger>
                      <SelectContent>
                        {teamMembers.map((member) => (
                          <SelectItem key={member.id} value={member.id}>
                            <div className="flex items-center gap-2">
                              <User className="w-4 h-4" />
                              {member.name}
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="taskStatus">Status</Label>
                    <Select
                      value={newTask.status}
                      onValueChange={(value: TaskStatus) =>
                        setNewTask((prev) => ({ ...prev, status: value }))
                      }
                      disabled={isCreating}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="To Do">To Do</SelectItem>
                        <SelectItem value="In Progress">In Progress</SelectItem>
                        <SelectItem value="Done">Done</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <DialogFooter className="flex gap-3">
                  <Button
                    variant="outline"
                    onClick={() => setIsCreateDialogOpen(false)}
                    disabled={isCreating}
                  >
                    Cancel
                  </Button>
                  <Button onClick={handleCreateTask} disabled={isCreating}>
                    {isCreating ? "Creating..." : "Create Task"}
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardHeader>

          <CardContent>
            {tasks.length === 0 ? (
              isLoading ? (
                <Loader2 className="mx-auto mt-2 animate-spin" size={24} />
              ) : (
                <div className="py-12 text-center">
                  <p className="mb-4 text-stone-500">No tasks found</p>
                  <p className="text-stone-400 text-sm">
                    Create a new task to get started
                  </p>
                </div>
              )
            ) : (
              <div className="border rounded-md">
                <table className="w-full text-sm caption-bottom">
                  <thead className="[&_tr]:border-b">
                    {table.getHeaderGroups().map((headerGroup) => (
                      <tr key={headerGroup.id}>
                        {headerGroup.headers.map((header) => (
                          <th
                            key={header.id}
                            className="px-4 h-12 font-medium text-stone-500 text-left align-middle"
                          >
                            {header.isPlaceholder
                              ? null
                              : flexRender(
                                  header.column.columnDef.header,
                                  header.getContext()
                                )}
                          </th>
                        ))}
                      </tr>
                    ))}
                  </thead>
                  <tbody className="[&_tr:last-child]:border-0">
                    {table.getRowModel().rows.map((row) => (
                      <tr
                        key={row.id}
                        className="hover:bg-stone-50 border-b transition-colors"
                      >
                        {row.getVisibleCells().map((cell) => (
                          <td key={cell.id} className="p-4 align-middle">
                            {flexRender(
                              cell.column.columnDef.cell,
                              cell.getContext()
                            )}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Project;
