+ 下载树莓派官方镜像[Raspbian](downloads.raspberrypi.org/raspbian_latest)或其他
+ 下载树莓派镜像烧写工具[win32diskimager](https://sourceforge.net/projects/win32diskimager/)
+ 烧写镜像到TF卡，注意不要在windows下格式化任何盘
+ 在/boot下编辑wpa_supplicant.conf配置默认wifi连接，配置如下:
```config
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
 
network={
    ssid="WIFI_NAME"
    psk="PASSWORD"
    key_mgmt=WPA-PSK
    priority=1
}
```

+ 在/boot下新建 ssh 文件(空文件且无扩展名)配置允许ssh连接
+ 启动树莓派，登录路由器管理页面查看IP地址
+ 使用[putty](https://pan.baidu.com/share/link?shareid=2217335081&uk=605377859) SSH 到树莓派，raspbian默认用户名/密码: pi/raspberry

+ 为树莓派更换国内镜像源
```
sudo nano /etc/apt/sources.list
```
用#注释掉原文件内容，用以下内容取代
```
# 清华大学源
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi 
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi 
```
> sudo apt-get update 更新源列表
+ 为树莓派添加远程桌面
```
sudo apt-get install xrdp
# 使用Windows自带mstsc即可远程桌面到树莓派
```
+ 为树莓派配置samba服务
```
# 更新源列表
sudo apt-get update
# 安装samba samba-common-bin
sudo apt-get install samba samba-comon-bin
# 备份并编辑samba配置文件
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.back
sudo vim /etc/samba/smb.conf
```
```
# 在末尾加入如下内容
# 分享名称
[MyNAS]
    # 说明信息
    comment = NAS Storage
    # 可以访问的用户
    valid users = pi,root
    # 共享文件的路径,raspbian 会自动将连接到其上的外接存储设备挂载到/media/pi/目录下
    path = /media/pi/
    # 可被其他人看到资源名称（非内容）
    browseable = yes
    # 可写
    writable = yes
    # 新建文件的权限为 664
    create mask = 0664
    # 新建目录的权限为 775
    directory mask = 0775
```
```
# 保存后设置用户名密码
sudo smbpasswd -a pi
# 重启samba 服务
sudo /etc/init.d/samba restart
# 设置开机自启
sudo nano /etc/rc.local
# 将命令 sudo /etc/init.d/samba restart添加到exit 0之前
```

+ 设置树莓派默认python版本
```
# 设置python3默认
sudo rm -rf /usr/bin/python
sudo ln -s /usr/bin/python3  /usr/bin/python
# 恢复python2 默认
sudo rm -rf /usr/bin/python
sudo ln -s /usr/bin/python2 /usr/bin/python
```

+ 安装Firefox浏览器
```
# linux中直接安装firefox-esr
sudo apt-get install firefox-esr
# 或Firefox衍生版
sudo apt-get install iceweasel
```
> 要做全屏效果的话, 可以加装插件[FF Fullscreen](https://addons.mozilla.org/en-US/firefox/addon/FF_Fullscreen/)

+ 安装中文输入法
```
# 安装字库
sudo apt-get install ttf-wqy-zenhei
# 安装输入法
sudo apt-get install scim-pinyin
# 设置本地语言环境
sudo raspi-config
# 然后选择change_locale
# 选择zh_CN.UTF-8,配置完成
# 重启
sudo reboot
```

+ 安装Node.js

> 下载已经[Node官网](https://nodejs.org/zh-cn/download/)编译好的node.js for ARM 最新版本, 树莓派3B选ARMv7
使用命令uname -a可查看该下载什么版本
```
wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-armv7l.tar.xz
# 解压文件
tar -xvf node-v10.16.0-linux-armv7l.tar.xz
# 验证node是否正常，屏幕打印v10.16.0说明正常
cd node-v10.16.0-linux-armv7l/bin
node -v
# 继续下一步
cd ~/
$ mv node-v6.9.4-linux-armv7l /usr/local/node
$ echo PATH=$PATH:/usr/local/node/bin >> ~/.bashrc
$ source .bashrc
# 现在任何位置均可使用node和npm了，大功告成！
```