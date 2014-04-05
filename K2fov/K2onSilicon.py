"""
Created on Wed Jan 29 10:40:14 2014

@author: tom_barclay


The code will accept a file containing a minimum of two columns
RA Dec.
where RA and Dec are in decimal degrees

"""
from __future__ import division, print_function
import sys
try:
    import numpy as np
except ImportError:
    print('You need numpy installed')
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    got_mpl = True
except ImportError:
    print('You need matplotlib installed to get a plot')
    got_mpl = False

import projection as proj
import  fov

__version__ = '0.0.1'

params = {#'backend': 'png',
                        'axes.linewidth': 1.5,
                        'axes.labelsize': 24,
                        'axes.font': 'sans-serif',
                        #'axes.fontweight' : 'bold',
                        'text.fontsize': 22,
                        'legend.fontsize': 14,
                        'xtick.labelsize': 16,
                        'ytick.labelsize': 16,
                        'text.usetex': False,
                        #'font.family': 'Palatino'
                        }
plt.rcParams.update(params)

#try:
#    plt.rcParams.update({'font.family': 'Palatino'})
#except:
#    pass


def angSepVincenty(ra1,dec1,ra2,dec2):
    """
    Vincenty formula for distances on a sphere
    """
    ra1_rad = np.radians(ra1)
    dec1_rad = np.radians(dec1)
    ra2_rad = np.radians(ra2)
    dec2_rad = np.radians(dec2)
    #diffpos = np.arccos(
    #    np.sin(dec1_rad)*np.sin(dec2_rad) +
    #    np.cos(dec1_rad)*np.cos(dec2_rad)*np.cos(np.abs(ra1_rad - ra2_rad)))

    sin_dec1, cos_dec1 = np.sin(dec1_rad), np.cos(dec1_rad)
    sin_dec2, cos_dec2 = np.sin(dec2_rad), np.cos(dec2_rad)
    delta_ra = ra2_rad - ra1_rad
    cos_delta_ra, sin_delta_ra = np.cos(delta_ra), np.sin(delta_ra)

    diffpos = np.arctan2(np.sqrt((cos_dec2 * sin_delta_ra) ** 2 +
                       (cos_dec1 * sin_dec2 -
                        sin_dec1 * cos_dec2 * cos_delta_ra) ** 2),
                  sin_dec1 * sin_dec2 + cos_dec1 * cos_dec2 * cos_delta_ra)

    return np.degrees(diffpos)


def parse_file(infile):
    try:
        a,b, mag = np.atleast_2d(np.genfromtxt(infile, usecols=[0,1,2],delimiter=',')).T
    except IOError:
        print('There seems to be a problem with the input file, the format should be: RA_degrees (J2000), \
            Dec_degrees (J2000), Magnitude. There should be no header, columns should be seperated by a comma')
        sys.exit(1)
    return a,b, mag

def onSiliconCheck(ra_deg,dec_deg,FovObj):
    try:
        ch = FovObj.pickAChannel(ra_deg, dec_deg)
        ch, col, row = FovObj.getChannelColRow(ra_deg, dec_deg)
        #exclude modules 3 and 7
        if ch in [5,6,7,8,17,18,19,20]:
            return False
        #return (ch,col,row)
        return True
    except ValueError:
        return False

def nearSiliconCheck(ra_deg,dec_deg,FovObj,max_sep=8.2):
    dist = angSepVincenty(FovObj.ra0_deg,FovObj.dec0_deg,ra_deg,dec_deg)
    if dist <= max_sep:
        return True
    else:
        return False


def getRaDecRollFromFieldnum(fieldnum):
    if fieldnum not in [0,1,2,3,4]:
        raise ValueError('Only Fields 0-4 are defined in this version of the code')
    elif fieldnum == 0:
        #ra_deg = 98.15766666666666
        #dec_deg = 21.594944444444444
        #scRoll_deg = 177.535
        ra_deg = 98.2964079
        dec_deg = 21.5878901
        scRoll_deg = 177.4810830
    elif fieldnum == 1:
        ra_deg = 173.939610
        dec_deg = 1.4172989
        scRoll_deg = 157.641206
    elif fieldnum == 2:
        ra_deg = 246.1264
        dec_deg = -22.4473
        scRoll_deg = 171.2284
    elif fieldnum == 3:
        ra_deg = 336.665346414
        dec_deg = -11.096663792
        scRoll_deg = -153.494818181
    elif fieldnum == 4:
        print('Warning, Field 4 position will change')
        ra_deg = 56.496
        dec_deg = 18.130472222222224
        scRoll_deg = 177.4810830
    else:
        raise NotImplementedError

    return (ra_deg, dec_deg, scRoll_deg)


# def run_test():
#     infile = 'KeplerCampaignMDwarfsTargetList.txt'
#     fieldnum = 0

#     ra_sources_deg, dec_sources_deg = parse_file(infile)
#     ra_deg, dec_deg, scRoll_deg = getRaDecRollFromFieldnum(fieldnum)
#     fovRoll_deg = fov.getFovAngleFromSpacecraftRoll(scRoll_deg)

#     k = fov.KeplerFov(ra_deg, dec_deg, fovRoll_deg)

#     raDec = k.getCoordsOfChannelCorners()


#     onSilicon = map(onSiliconCheck,
#         ra_sources_deg,dec_sources_deg,np.repeat(k,len(ra_sources_deg)))

#     nearSilicon = map(nearSiliconCheck,
#         ra_sources_deg,dec_sources_deg,np.repeat(k,len(ra_sources_deg)))

#     onSilicon = np.array(onSilicon,dtype=bool)
#     nearSilicon = np.array(nearSilicon, dtype=bool)

#     if got_mpl:
#         ph = proj.Cylindrical()
#         k.plotPointing(ph,showOuts=False)
#         targets = ph.skyToPix(ra_sources_deg, dec_sources_deg)
#         fig = plt.gcf()
#         ax = fig.gca()
#         ax = fig.add_subplot(111)
#         ax.scatter(*targets,s=0.5)
#         ax.scatter(targets[0][nearSilicon],
#             targets[1][nearSilicon],color='b')
#         ax.scatter(targets[0][onSilicon],
#             targets[1][onSilicon],color='r')
#         ax.set_xlabel('R.A. [radians]',fontsize=16)
#         ax.set_ylabel('Declination [radians]',fontsize=16)




#         fig.show()


def K2onSilicon(infile,fieldnum):
    ra_sources_deg, dec_sources_deg, mag = parse_file(infile)

    if np.shape(ra_sources_deg)[0] > 500:
        print('There are {} sources in your target list, this could take some time'.format(np.shape(ra_sources_deg)[0]))

    ra_deg, dec_deg, scRoll_deg = getRaDecRollFromFieldnum(fieldnum)

    ## convert from SC roll to FOV coordinates
    ## do not use the fovRoll coords anywhere else
    ## they are internal to this script only
    fovRoll_deg = fov.getFovAngleFromSpacecraftRoll(scRoll_deg)

    ## initialize class
    k = fov.KeplerFov(ra_deg, dec_deg, fovRoll_deg)

    raDec = k.getCoordsOfChannelCorners()


    onSilicon = map(onSiliconCheck,
        ra_sources_deg,dec_sources_deg,np.repeat(k,len(ra_sources_deg)))

    nearSilicon = map(nearSiliconCheck,
        ra_sources_deg,dec_sources_deg,np.repeat(k,len(ra_sources_deg)))

    onSilicon = np.array(onSilicon,dtype=bool)
    nearSilicon = np.array(nearSilicon, dtype=bool)

    if got_mpl:
        almost_black = '#262626'
        light_grey = np.array([float(248)/float(255)]*3)
        ph = proj.Cylindrical()
        k.plotPointing(ph,showOuts=False,plot_degrees=True)
        targets = ph.skyToPix(ra_sources_deg, dec_sources_deg)
        targets = np.array(targets ) * 180 / np.pi
        fig = plt.gcf()
        ax = fig.gca()
        ax = fig.add_subplot(111)
        ax.scatter(*targets,s=2,label='not on silicon')
        ax.scatter(targets[0][nearSilicon],
            targets[1][nearSilicon],color='#fc8d62',s=8,label='near silicon')
        ax.scatter(targets[0][onSilicon],
            targets[1][onSilicon],color='#66c2a5',s=8,label='on silicon')
        ax.set_xlabel('R.A. [degrees]',fontsize=16)
        ax.set_ylabel('Declination [degrees]',fontsize=16)
        ax.invert_xaxis()
        ax.minorticks_on()
        legend = ax.legend(loc=0,
            frameon=True, scatterpoints=1)
        rect = legend.get_frame()
        rect.set_alpha(0.3)
        rect.set_facecolor(light_grey)
        rect.set_linewidth(0.0)
        texts = legend.texts
        for t in texts:
            t.set_color(almost_black)
        fig.savefig('targets_fov.png',dpi=300)
        plt.close('all')

    siliconFlag = np.zeros_like(ra_sources_deg)
    siliconFlag = np.where(nearSilicon,1,siliconFlag)
    siliconFlag = np.where(onSilicon,2,siliconFlag)

    outarr = np.array([ra_sources_deg, dec_sources_deg, mag, siliconFlag])
    np.savetxt('targets_siliconFlag.csv', outarr.T, delimiter=', ',
        fmt=['%10.10f','%10.10f','%10.2f','%i'])

    if got_mpl:
        print('I made two files: targets_siliconFlag.csv and targets_fov.png')
    else:
        print('I made one file: targets_siliconFlag.csv')





if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('')
        print('python K2onSilicon.py filename fieldnum')
        print('')
        sys.exit(2)
    elif len(sys.argv) != 3:
        print('use the command')
        print('python K2onSilicon.py filename fieldnum')
        sys.exit(2)

    fieldnum = int(sys.argv[2])
    infile = str(sys.argv[1])

    K2OnSilicon(infile, fieldnum)








