; Inno Setup 脚本：NiceProgram App 安装程序
; 用法: "D:\InnoSetup\InstallPath\ISCC.exe" NiceProgram_installer.iss
; 输出: dist/NiceProgram_Setup_1.0.0.exe

#define MyAppName "NiceProgram App"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Hydrooxygen"
#define MyAppExeName "App.exe"
#define MyAppURL "https://github.com/Hydrooxzgen"

[Setup]
AppId={{8B4F0B3A-1E9D-4C3A-9B2E-5F6A7D8C9E0F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\NiceProgram
DefaultGroupName=NiceProgram
DisableProgramGroupPage=yes
; 用户数据(UserFiles)放在程序目录旁，卸载时保留用户数据
UninstallDisplayIcon={app}\{#MyAppExeName}
; 压缩设置
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; 输出
OutputDir=dist
OutputBaseFilename=NiceProgram_Setup_{#MyAppVersion}
; 安装到 Program Files 需要管理员权限（默认 admin 模式即可）
PrivilegesRequired=admin
; 中文界面
SetupIconFile=
; 版本信息
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=NiceProgram App 安装程序
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
; 不强制关闭正在运行的程序（提示用户）
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 打包产物：整个 NiceProgram 目录（含 exe 与 _internal，模板在 _internal/UserFiles/template）
Source: "dist\NiceProgram\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意：程序目录的 UserFiles 由程序首次启动时自动创建，此处不打包

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 卸载时删除程序目录中的 UserFiles 用户数据（可选，如要保留请删除本段）
Type: filesandordirs; Name: "{app}\UserFiles"
