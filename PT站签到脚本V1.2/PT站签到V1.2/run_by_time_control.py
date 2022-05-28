from apscheduler.schedulers.blocking import BlockingScheduler
import PT_Visit_Sign,analysis_config

def strif_hour_minute_seconds(raw:int) -> str:
    return str(raw) if raw >= 10 else '0' + str(raw)

if __name__ == '__main__':
    my_config_dict = analysis_config.read_config()
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    day_of_week = my_config_dict['定时']['周几至周几']
    hour = int( my_config_dict['定时']['时'] )
    minitue = int( my_config_dict['定时']['分'] )
    print('正在运行定时签到，时间规则：\n每周{} {}:{} 执行签到'.format(day_of_week,strif_hour_minute_seconds(hour),strif_hour_minute_seconds(minitue) ) )
    #↓调整计算周几至周几,以适应scheduler.add_job day_of_week参数要求 最大0-6
    start_week,end_week = day_of_week.split('-')
    start_week = str ( int( start_week ) -1 )
    end_week = str ( int( end_week ) -1 )
    day_of_week = start_week + '-' + end_week
    scheduler.add_job( PT_Visit_Sign.visit_and_signin_all_websites , 'cron', day_of_week=day_of_week, hour=hour, minute=minitue ,args = [ my_config_dict ])
    scheduler.start()