#!/usr/bin/env python

#import C_Python
import requests
from requests.auth import HTTPBasicAuth
import re

class BuildInfo:
    branch_name = 'sl_master'
    startDate = ''
    endDate = '' 
    url = "https://ctgbuild-test.cisco.com/cerebro7webservices/getBuildsReport?startDate=6-1-2018&endDate=6-15-2018&buList=PHONE"   
    def __init__(self,name,start,end):
        self.branch_name = name
        self.startDate = start
        self.endDate = end
        url = self.url.split('?')
        print url
        self.url = url[0] + '?startDate='+self.startDate+'&endDate='+self.endDate+'&buList=PHONE'
        print 'new self.url:%s' % self.url


    def getOverallBuild(self):
        requests.adapters.DEFAULT_RETRIES = 3
        requests.Timeout = 10
        user_agent={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}  
        response = requests.get(self.url, user_agent)#, auth=HTTPBasicAuth('ronling','weblxjhuQ~4'))

        exp_str = r'(\d{6},\d{4},PHONE,'+self.branch_name+',)'
        pattern_all = re.compile(exp_str,re.DOTALL)
        #print re.search(pattern_all,response.content).string
        count_overall = len(re.findall(pattern_all,response.content))
        print 'The overall build is: %d' % count_overall
        return count_overall

    def getPassedBuild(self):
        requests.adapters.DEFAULT_RETRIES = 3
        requests.Timeout = 10
        user_agent={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}  
        response = requests.get(self.url, user_agent)#, auth=HTTPBasicAuth('ronling','weblxjhuQ~4'))

        exp_str = r'(\d{6},\d{4},PHONE,'+self.branch_name+',[^,]*,[^,]*,Passed)'
        pattern_failure = re.compile(r'(\d{6},\d{4},PHONE,sl_master,[^,]*,[^,]*,Passed)',re.DOTALL)
        print re.findall(pattern_failure,response.content)
        count_passed = len(re.findall(pattern_failure,response.content))
        print 'The passed build is: %d' % count_passed
        return count_passed

    def getPassedRatio(self):
        build_all = self.getOverallBuild()
        build_passed = self.getPassedBuild()
        pass_rate = (build_passed*100)/build_all  
        print 'The build pass rate (on %s) is:%s percent' % (self.branch_name,pass_rate)
        return pass_rate

if __name__ == '__main__':
    build_info = BuildInfo('slm_mppmr2','12-10-2017','6-15-2018')
    build_info.getPassedRatio()
