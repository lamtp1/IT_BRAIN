import { TaskService } from './task.service';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
export declare class TaskController {
    private readonly taskService;
    constructor(taskService: TaskService);
    create(createTaskDto: CreateTaskDto): {
        title: string;
        description: string;
        dueDate: Date;
        assignedTo: string;
        id: number;
    };
    findAll(): any[];
    findOne(id: string): any;
    update(id: string, updateTaskDto: UpdateTaskDto): any;
    remove(id: string): any[];
}
