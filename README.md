确保你已经在包的根目录：进入包含 pyproject.toml 文件的目录（通常是项目根目录，比如 gurddy/）。
运行本地安装命令：
`pip install .`

这个命令会从当前目录构建并安装包。
如果你想在开发模式下安装（可编辑代码而不需重新安装），可以用：
`pip install -e .`

验证安装：
安装后，你可以运行以下命令检查：
`pip list | grep gurddy`
如果显示 gurddy 及其版本，说明安装成功。然后在 Python 代码中导入使用：
`import gurddy`
如果遇到问题（如缺少依赖），确保你的 Python 环境有必要的库（如 PuLP，用于 LP 求解器）。如果需要，我可以帮你调试代码或添加更多功能！