"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskService = void 0;
const common_1 = require("@nestjs/common");
let TaskService = class TaskService {
    constructor() {
        this.tasks = [];
    }
    create(createTaskDto) {
        const newTask = Object.assign({ id: Date.now() }, createTaskDto);
        this.tasks.push(newTask);
        return newTask;
    }
    findAll() {
        return this.tasks;
    }
    findOne(id) {
        return this.tasks.find((task) => task.id === id);
    }
    update(id, updateTaskDto) {
        const taskIndex = this.tasks.findIndex((task) => task.id === id);
        if (taskIndex === -1)
            return null;
        this.tasks[taskIndex] = Object.assign(Object.assign({}, this.tasks[taskIndex]), updateTaskDto);
        return this.tasks[taskIndex];
    }
    remove(id) {
        const taskIndex = this.tasks.findIndex((task) => task.id === id);
        if (taskIndex === -1)
            return null;
        return this.tasks.splice(taskIndex, 1);
    }
};
TaskService = __decorate([
    (0, common_1.Injectable)()
], TaskService);
exports.TaskService = TaskService;
//# sourceMappingURL=task.service.js.map