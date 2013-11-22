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
    if (month==0): return 5;
    if (month==1): return 5;
    if (month==2): return 5;
    if (month==3): return 5;
    if (month==4): return 5;
    if (month==5): return 5;
    if (month==6): return 5;
    if (month==7): return 5;
    if (month==8): return 5;
    if (month==9): return 5;
    if (month==10): return 5;
    if (month==11): return 5;
    return 6;

def pump(power,month):
    Q1=0;
# head/flowrate in l/min curve for the Agnimotors 3x3 inch prototype; return hourly liters
    if depth(month)==3: Q1=680;
    if depth(month)==4: Q1=630;
    if depth(month)==5: Q1=624;
    if depth(month)==6: Q1=580;
#estimated 
    if depth(month)==7: Q1=500; #*1/sqrt(6/7);
    if depth(month)==8: Q1=0; #*1/sqrt(6/8);
#    print faktor;
#    print Q1;
# factors for lower then optimal power of the pump
# NEW: use of the affinity laws (see http://en.wikipedia.org/wiki/Affinity_laws)
# - flow is proportional to shaft speed: Q1/Q2=N1/N2
# - head (pressure) is proportional to the square of the shaft speed: H1/H2=(N1/N2)^2
# - power is proportional to the cube of the shaft speed: P1/P2=(N1/N2)^3
    faktor=0;
    newhead=0;
# no flow for <600 W @5m head (affinity laws) of solar power    
    if depth(month)==5: 
        if (power<600.0):
             Q1=0;
    if depth(month)==6: 
        if (power <750.0):
             Q1=0;    
    faktor=(power/750.0)**(float(1.0/3.0));
    return Q1*faktor*60.0;
    
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

