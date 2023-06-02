# This Python file uses the following encoding: utf-8
# @author runhey
# github https://github.com/runhey

from module.gui.utils import check_admin
from module.gui.context.add import Add
from module.gui.context.settings import Setting
from module.gui.context.process_manager import ProcessManager
from module.gui.fluent_app import FluentApp

if __name__ == "__main__":
    # 检查是不是以管理员身份运行，脚本启动的其他进程会继承权限
    # 但是貌似有问题的这个函数
    # check_admin()
    # 启动一个UI交互的线程，因为信号槽不可跨进程
    # 后面选择注入上下文快
    app = FluentApp()
    add_config = Add()
    setting = Setting()
    process_manager = ProcessManager()

    app.set_context_property(setting, 'setting')
    app.set_context_property(add_config, 'add_config')
    app.set_context_property(process_manager, 'process_manager')
    # 启动一个GUI
    app.run()
