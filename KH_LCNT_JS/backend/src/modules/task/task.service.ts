import { Injectable } from '@nestjs/common';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';

@Injectable()
export class TaskService {
  private tasks = [];

  create(createTaskDto: CreateTaskDto) {
    const newTask = { id: Date.now(), ...createTaskDto };
    this.tasks.push(newTask);
    return newTask;
  }

  findAll() {
    return this.tasks;
  }

  findOne(id: number) {
    return this.tasks.find((task) => task.id === id);
  }

  update(id: number, updateTaskDto: UpdateTaskDto) {
    const taskIndex = this.tasks.findIndex((task) => task.id === id);
    if (taskIndex === -1) return null;

    this.tasks[taskIndex] = { ...this.tasks[taskIndex], ...updateTaskDto };
    return this.tasks[taskIndex];
  }

  remove(id: number) {
    const taskIndex = this.tasks.findIndex((task) => task.id === id);
    if (taskIndex === -1) return null;

    return this.tasks.splice(taskIndex, 1);
  }
}