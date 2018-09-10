"""
Main module

"""
# Copyright 2018 European Union
# This file is part of [software name], a software written by [author's name] ([JRC unit])
# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence").
# Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the Licence for the specific language governing permissions and limitations under the Licence. 


import os
import glob
from pyPoseidon.utils.get_value import get_value

class wrf:
    
    def __init__(self, **kwargs):
        
        self.tag = kwargs.get('tag', None)
        self.mpath = kwargs.get('mpath', None)
        self.wrf_path = kwargs.get('WRF_PATH', None)
        self.meteo = kwargs.get('meteo', None)
        

        if self.meteo == 'erai' :
            self.metgrid='METGRID.TBL.ERAI'
        elif self.meteo == 'ecmwf' :
            self.metgrid='METGRID.TBL.ARW'

        rpath = get_value(self,kwargs,'rpath','./') 


        if not os.path.exists(rpath):
            os.makedirs(rpath)  # create top folder
        
        if not os.path.exists(rpath+'/wps'):
            os.makedirs(rpath+'/wps')  # create wps folder

        if not os.path.exists(rpath+'/wrf'):
            os.makedirs(rpath+'/wrf')  # create wrf folder


#cp -uvr /usr/local/share/WRF/WRF3/WPS/namelist.wps  $case/wps/namelist.wps

#links
        cfiles = glob.glob(self.wrf_path+'/WPS/*.exe')
        for filename in cfiles:
                os.symlink(filename,rpath+'/wps'+filename)

        os.symlink(self.wrf_path+'/WPS/geogrid',rpath+'/wps/geogrid')

        os.symlink(self.wrf_path+'/WPS/link_grib.csh',rpath+'/wps/link_grib.sh')

        os.symlink(self.wrf_path+'/WPS/metgrid/'+self.metgrid, self.wrf_path+'/WPS/metgrid/METGRID.TBL')

        os.symlink(self.wrf_path+'/WPS/metgrid',rpath+'/wps/metgrid')

#link Vtable
        os.symlink(self.wrf_path+'/Vtable',rpath+'/wps/Vtable')
        
        
#setup wrf folder
        os.symlink(self.wrf_path+'run',rpath+'/wps/Vtable')

        cfiles = glob.glob(wrf_path+'/WRFV3/run/*_DATA')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)
    
        cfiles = glob.glob(wrf_path+'/WRFV3/run/ETAMP*')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        cfiles = glob.glob(wrf_path+'/WRFV3/run/*.TBL')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        cfiles = glob.glob(wrf_path+'/WRFV3/run/tr*')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)
            
        cfiles = glob.glob(wrf_path+'/WRFV3/run/*.txt')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        cfiles = glob.glob(wrf_path+'/WRFV3/run/*.tbl')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        cfiles = glob.glob(wrf_path+'/WRFV3/run/*.formatted')
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        cfiles = glob.glob(wrf_path+'/WRFV3/main/*.exe)
        for filename in cfiles:
            os.symlink(filename,rpath+'/wrf/'+filename)

        
        
        def namelist(self,**kwargs):
            
# namelists

        

#link namelists for geogrid
for namelist in $data_path/namelist*.wps;

        do

            ln -sf $current_dir/$namelist   $case/wps/namelist.wps

            echo 'executing geogrid for '$namelist
            #execute geogrid 
            cd $case/wps && ./geogrid.exe

            break

        done
            

#link namelists for ungrib
for namelist in $current_dir/$data_path/namelist*.wps;
        
        do

            v2=${namelist:0:-4}

            k=${v2: -1}

            ln -sf $namelist   $current_dir/$case/wps/namelist.wps

            echo 'link data'
            #link data
            
            if [ $k -eq 1 ] 
            then
                echo 'linking $current_dir/$data_path/DATA/EPRES_HEMI* files'
                ./link_grib.sh $current_dir/$data_path/DATA/EPRES_HEMI*
            elif [ $k -eq 2 ] 
            then
                 echo 'linking $current_dir/$data_path/DATA/ESFC_HEMI* files'
                ./link_grib.sh $current_dir/$data_path/DATA/ESFC_HEMI*
            fi

            echo 'executing ungrib for '$namelist

            ./ungrib.exe

            for griblink in ./GRIBFILE.*;

            do
               rm $griblink
            done


        done

#execute metgrid 
./metgrid.exe

# return to top dir
cd $current_dir



ln -sf $current_dir/$data_path/namelist.input   $case/wrf/namelist.input


#link wps output
ln -sf $current_dir/$case/wps/met_em.d01*  $case/wrf/
ln -sf $current_dir/$case/wps/met_em.d02*  $case/wrf/
ln -sf $current_dir/$case/wps/met_em.d03*  $case/wrf/


