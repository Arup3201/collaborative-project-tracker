export type TaskStatus = 'To Do' | 'In Progress' | 'Completed';

export interface Task {
  id: string;
  name: string;
  description: string;
  deadline: string;
  assignee: string;
  status: TaskStatus;
}

export interface NewTaskData {
  name: string;
  description: string;
  deadline: string;
  assignee: string;
  status: TaskStatus;
}

export interface TeamMember {
  id: string;
  name: string;
  email: string;
}