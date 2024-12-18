import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
export declare class TaskService {
    private tasks;
    create(createTaskDto: CreateTaskDto): {
        title: string;
        description: string;
        dueDate: Date;
        assignedTo: string;
        id: number;
    };
    findAll(): any[];
    findOne(id: number): any;
    update(id: number, updateTaskDto: UpdateTaskDto): any;
    remove(id: number): any[];
}
