import json
import os
import logging
import datetime
import sys
import time
import shutil
from types import coroutine

class CopyBin:
    basic_config=\
    [
        "source_path",
        "target_path",
        "file_name",
        "series",
        "remark",
        "model",
        "currect"
    ]



    def __init__(self):
        # log 初始化
        self.logger=self.logging_init()

        # 加载config
        self.ConfigLoad()
        
        # 文件夹安全检查
        self.FilesSecurityCheck()


        self.optition_dict={
            "1":{
                "work":self.Optition_1_Function,
                "info":"\t1.从源文件夹复制到目标文件夹\n"
            },
            "2":{
                "work":self.Optition_2_Function,
                "info":"\t2.查看目前备份信息(请不要删除备份中的info.json信息文件)\n"
            },
            "3":{
                "work":self.Optition_3_Function,
                "info":"\t3.从保存的库中还原到目标路径中\n"
            }
        }
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))


        return 

      # log init 
    def logging_init(self):
        self.log_path="./logs/"
        logger = logging.getLogger(__name__)

        # ++
        # Log等级总开关
        logger.setLevel(logging.INFO)  
        # ++

        # 日志控制台输出
        stream_handler = logging.StreamHandler()  
        stream_handler.setLevel(logging.ERROR)
        # 设置控制台格式
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s : %(message)s')
        stream_handler.setFormatter(formatter)

        
        # log 存放设置
        log_name=datetime.datetime.strftime(datetime.datetime.now(),'%Y_%m_%d_%H_%M_%S')+".log"
        if not (os.path.exists(self.log_path)):
            os.mkdir(self.log_path)
            logger.info("mkdir "+self.log_path)

        # 文件渠道
        file_handler = logging.FileHandler(self.log_path+log_name)
        file_handler.setLevel(logging.INFO)

        # 更改logging在储存到txt的结构
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s : %(message)s')
        file_handler.setFormatter(formatter)

        # 绑定文件输出和控制台输出
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return logger

    def ConfigLoad(self):
        # config security check 
        if not (os.path.exists('./config.json')):
            self.logger.error("ERROR!!!\nconfig file no found!!")
            os.system("pause")
            os._exit(0)
        
        # 加载 config文件
        with open('./config.json','r',encoding='utf8')as fp:
            try:
                self.config = json.load(fp)
            except:
                self.logger.error("Error: Config is Empty")
                os.system("pause")
                os._exit(0)
        fp.close()

        # config 文件安全检查
        for config_name in self.basic_config:
            try:
                a=self.config[config_name]
            except:
                self.logger.error("Can not find config \"{}\"".format(config_name))
                os.system("pause")
                os._exit(0)
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))

     # 文件夹安全检查
    def FilesSecurityCheck(self):
        # 源文件文件夹
        if not (os.path.exists(self.config["source_path"])):
            os.mkdir(self.config["source_path"])
            self.logger.info("mkdir "+self.config["source_path"])

        # 保存文件夹
        if not (os.path.exists(self.config["save_path"])):
            os.mkdir(self.config["save_path"])
            self.logger.info("mkdir "+self.config["save_path"])

        # 目标文件夹
        for target_dir in self.config["target_path"]:
            if not (os.path.exists(target_dir)):
                os.mkdir(target_dir)
                self.logger.info("mkdir "+target_dir)
        '''
        #record json
        if not (os.path.exists(self.config["record_file"])):
            file=open(self.config["record_file"],"w")
            file.close()
            self.logger.info("mkdir "+self.config["record_file"])

        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        '''

    # 界面
    def InterFace(self):
        print("\n\t请输入选项：\n")
        length=len(self.optition_dict)
        #print(length)
        for i in range(length):
            print(self.optition_dict[str(i+1)]["info"])
        option=input("\t请输入：")

        # 执行函数
        try:
            p=self.optition_dict[str(option)]["work"]
        except:
            self.logger.error("Can not find optition \"{}\"".format(option))
            os.system("pause")
            os._exit(0)

        try:
            p()
        except:
            self.logger.error("optition \"{}\" error".format(option))
            os.system("pause")
            os._exit(0)

    # 获取当前时间
    def GetNowTime(self):
        
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 获取修改时间
    def GetChangeTime(self,filepath_filename):
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return (os.path.getmtime(filepath_filename))

    # 获取格式化修改时间
    def GetChangeTimeFormat(self,filepath_filename):
        t =time.localtime(self.GetChangeTime(filepath_filename))
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return "{}_{}_{}_{}_{}".format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min)

    # 获取常规修改时间
    def GetChangeTimeNomal(self,filepath_filename):
        t =time.localtime(self.GetChangeTime(filepath_filename))
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return "{}-{}-{} {}:{}".format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min)
    #
    #功能实现

    # 复制一个文件到一个文件夹中
    def CopyFileToDir(self,filepath_filename,dir_path):
        shutil.copy2(filepath_filename,dir_path)
        self.logger.info("{} copy to {}".format(filepath_filename,dir_path))
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))

    # 复制所有文件到所有文件夹中
    def CopyALLFileToTargetDir(self):
        # 遍历文件夹
        for dir in self.config["target_path"]:
            for file in self.config["file_name"]:
                if not (os.path.exists(self.config["source_path"]+file)):
                    self.logger.info("{} no exist ,skipped".format(self.config["source_path"]+file))
                    continue
                self.CopyFileToDir(self.config["source_path"]+file,dir)
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
                
    # 创建保存的文件夹
    def CreateBackupDir(self,change_time):
        filename="v{}_{}"\
                .format(
                    self.config["currect"],
                    change_time
                    )
        self.backup_dir=self.config["save_path"]+filename+"/"
        self.backup_dir_name = filename
        # 创建文件夹
        if not (os.path.exists(self.backup_dir)):
            os.mkdir(self.backup_dir)


        self.logger.info("Create Backup dir {}".format(str(self.config["currect"])+change_time))
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return

    # 备份文件
    def BackUpFiles(self,dir_path):
        for file in self.config["file_name"]:
            if not (os.path.exists(self.config["source_path"]+file)):
                self.logger.info("{} no exist ,skipped".format(self.config["source_path"]+file))
                continue
            self.CopyFileToDir(self.config["source_path"]+file,dir_path)

        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return



    # 更新CurrectNum
    def UpdateCurrectNum(self):
        self.config["currect"]=self.config["currect"]+1

        # 写 config文件
        with open('./config.json','w',encoding='utf8')as fp:
            json.dump(self.config,fp,indent=4)
        fp.close()

        # 重新更新
        with open('./config.json','r',encoding='utf8')as fp:
            self.config = json.load(fp)
        fp.close()
        return 



    # info文件相关功能
    def InfoInit(self):
        info=dict()
        info["series"]=self.config["series"]
        info["remark"]=self.remark
        info["model"]=self.config["model"]
        info["dir"]=self.backup_dir_name
        info["FW_num"]=self.FW_num
        info["version_num"]=self.version_num
        info["time"]=self.GetChangeTimeNomal(self.config["source_path"]+self.config["file_name"][0])
    
        return info

    # 添加info文件
    def AddInfoFile(self,filepath_filename,info):

        # 创建info.json
        if not (os.path.exists(filepath_filename)):
            file=open(filepath_filename,"w")
            file.close()
            self.logger.info("mkdir "+filepath_filename)

        # 写 config文件
        with open(filepath_filename,'w',encoding='utf8')as fp:
            json.dump(info,fp,indent=4)
        fp.close()

        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return

    # 复制功能
    def Copy(self):
        # 复制到目标地址
        self.CopyALLFileToTargetDir()

        # 备份
        # 修改时间
        change_time=self.GetChangeTimeFormat(self.config["source_path"]+self.config["file_name"][0])

        # 创建备份文件夹
        self.CreateBackupDir(change_time)

        # 备份
        self.BackUpFiles(self.backup_dir)

        # 添加info
        info=self.InfoInit()
        self.AddInfoFile(self.backup_dir+"info.json",info)

        # 更新currect
        self.UpdateCurrectNum()
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))


    # 遍历所有文件夹
    def GetAllDir(self,dir_path):
        for root,dirs,files in os.walk(dir_path):
            self.logger.info("Get dir {}".format(dirs))
            self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
            return dirs

    # 打印一个info
    def PrintOneInfo(self,dir_name,No,filepath_filename):
        # 打开info文件
        info_file=self.config["save_path"]+dir_name+"/"+"info.json"

        # 打开info文件
        with open(info_file,'r',encoding='utf8')as fp:
            try:
                info = json.load(fp)
            except:
                self.logger.info("{} is None".format(info_file))
        fp.close()

        # 显示info
        print("\t-----------------------------------")
        print("\t|\t")
        print("\t|\t{}. {}".format(No,info["dir"]))
        print("\t|\t{}  {}{} ".format(info["model"],info["series"],info["version_num"]))
        print("\t|\tbuild at {} ".format(info["time"]))
        print("\t|\t")
        print("\t|\t\t{}".format(info["remark"]))
        print("\t|\t")
        print("\t-----------------------------------")

        with open(filepath_filename,'a',encoding='utf8')as fp:
            fp.write("-----------------------------------\n")
            fp.write("\n")
            fp.write("{}. {}\n".format(No,info["dir"]))
            fp.write("{}  {}{} \n".format(info["model"],info["series"],info["version_num"]))
            fp.write("build at {} \n".format(info["time"]))
            fp.write("\n")
            fp.write("\t{}\n".format(info["remark"]))
            fp.write("\n")
            fp.write("-----------------------------------\n")

        fp.close()
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))


    # 打印info文件
    def PrintInfo(self):

        # 创建all info文件
        if not (os.path.exists("./AllInfo.txt")):
            file=open("./AllInfo.txt","w")
            file.close()
            self.logger.info("mkdir ./AllInfo.txt")
        
        # 清空文件
        with open("./AllInfo.txt",'w',encoding='utf8')as fp:
            fp.write("")
        fp.close()

        dirs=self.GetAllDir(self.config["save_path"])
        count=0
        for dir in dirs:
            count=count+1
            self.PrintOneInfo(dir,count,"./AllInfo.txt")
        #for dir in self.config["save_path"]:
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        return
    
    # 复制所有文件到所有文件夹中
    def CopyALLFileFromSaveDirToTargetDir(self,save_dir_name):
        # 遍历文件夹
        for dir in self.config["target_path"]:
            # 遍历目标文件
            for file in self.config["file_name"]:
                if not (os.path.exists(self.config["save_path"]+save_dir_name+"/"+file)):
                    self.logger.info("{} no exist ,skipped".format(self.config["save_path"]+save_dir_name+"/"+file))
                    continue
                # 复制
                self.CopyFileToDir(self.config["save_path"]+save_dir_name+"/"+file,dir)
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))

    # 还原版本
    def Revert(self,save_dir_name):
        if(save_dir_name == ""):
            self.logger.info("save_dir_name not exists")
            print("文件名不存在，请检查路径")
            os.system("pause")
            os._exit(0)

        if not (os.path.exists(self.config["save_path"]+save_dir_name+"/")):
            self.logger.info("{} not exists".format(self.config["save_path"]+save_dir_name+"/"))
            print("{} 不存在，请检查路径".format(self.config["save_path"]+save_dir_name+"/"))
            os.system("pause")
            os._exit(0)
        
        # 开始复制
        self.CopyALLFileFromSaveDirToTargetDir(save_dir_name)



    # 选项对应的函数接口
    def Optition_1_Function(self):
        self.version_num=input("\t请输入{}号：".format(self.config["series"]))
        self.FW_num=input("\t请输入FW号:")
        self.remark=input("\t请输入备注：")
        if(self.remark==""):
            print("请输入备注,操作终止.....\n")
            self.logger.error("no remark input")
            os.system("pause")
            os._exit(0)
        self.Copy()
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        os.system("pause")
        return

    def Optition_2_Function(self):
        self.PrintInfo()
        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        os.system("pause")
        return

    def Optition_3_Function(self):
        self.Revert(input("\t请输入需要还原的文件夹名称："))

        self.logger.info("{} finished".format(sys._getframe().f_code.co_name))
        print("还原完成")
        os.system("pause")
        return



if __name__=="__main__":
    cb=CopyBin()
    cb.InterFace()

