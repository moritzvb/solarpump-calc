#!/usr/bin/python  


# (C) 2013 Moritz v. Buttlar, moritz@opensource-solar.org
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
                
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
                        
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
                                        
                                        

import csv     	# imports the csv module
import sys      # imports the sys module


# this function defines the depth of the water for each month
def depth(month):
    if (month==0): return 6;
    if (month==1): return 6;
    if (month==2): return 6;
    if (month==3): return 6;
    if (month==4): return 5;
    if (month==5): return 5;
    if (month==6): return 5;
    if (month==7): return 5;
    if (month==8): return 6;
    if (month==9): return 6;
    if (month==10): return 6;
    if (month==11): return 6;
    return 5;

def pump(power,month):
# factors for lower then optimal power of the pump
    faktor=0;
    if (power>=740):
        faktor=1;
    if ((power>600) & (power<=739)):
        faktor=0.8;
    if ((power>500) & (power<=600)):
        faktor=0.7;
    if ((power>400) & (power<=500)):
        faktor=0.4;
    if ((power>300) & (power<=400)):
        faktor=0.0;
# head/flowrate in l/min curve for the Agnimotors 3x3 inch prototype; return hourly liters
    if depth(month)==3: return 680*faktor*60;
    if depth(month)==4: return 630*faktor*60;
    if depth(month)==5: return 624*faktor*60;
    if depth(month)==6: return 580*faktor*60;
#estimated
    if depth(month)==7: return 500*faktor*60;
    if depth(month)==8: return 400*faktor*60;
    print 'error'
    return 0;
    
f = open(sys.argv[1], 'rb') # opens the csv file
# solar array area [m^2]
area=8;
# panel efficiency [Percent]
eff=18;
# power_peak
power_peak=8*1000*0.18;

try:
    reader = csv.reader(f)  # creates the reader object
    oldDate="Header";
    firstDate="first";
    dayLiters=0;
    a=0;
    month=0;
    monthDayCount=0;
    monthLiters=0;
    for row in reader:   # iterates the rows of the file in orders
        a=a+1;
        if (a>2):		# the first two lines are headers, so skip them
            date=row[0];
            time=row[1];
            etr=row[2];
            etrn=row[3];
            ghi=row[4];
            a1=row[5];
            a2=row[6];            
            norm=float(row[7])*0.95;	# cos(30 deg) = 0.95; 30 degrees miss-alignment max., 5 % loss; realign every 2 hours
            pwr=norm*power_peak/1000;
            # calculate the liters pumped in this hour 
            dayLiters=dayLiters+pump(pwr,month);
            # check if next day started
            if (date!=oldDate):
#                print dayLiters;
                monthLiters=monthLiters+dayLiters
                dayLiters=0;
#                print date
                oldDate=date
                monthDayCount=monthDayCount+1;
#		assume 30 days/month on average to keep things simple                
                if (monthDayCount>29):                
                    print int(monthLiters/1000); # print result in cubic meters (1000 l)
                    month=month+1;
                    monthLiters=0;
                    monthDayCount=0;
finally:
    f.close()      # closi

