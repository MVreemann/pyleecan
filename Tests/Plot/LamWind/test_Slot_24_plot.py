# -*- coding: utf-8 -*-
"""
@date Created on Tue Jan 12 13:54:56 2016
@copyright (C) 2015-2016 EOMYS ENGINEERING.
@author pierre_b
"""

from os.path import join
from unittest import TestCase

import matplotlib.pyplot as plt
from numpy import array, pi, zeros

from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.LamSquirrelCage import LamSquirrelCage
from pyleecan.Classes.Machine import Machine
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.VentilationCirc import VentilationCirc
from pyleecan.Classes.VentilationPolar import VentilationPolar
from pyleecan.Classes.VentilationTrap import VentilationTrap
from pyleecan.Classes.Winding import Winding
from pyleecan.Classes.WindingUD import WindingUD
from pyleecan.Classes.WindingCW2LT import WindingCW2LT
from pyleecan.Classes.WindingDW2L import WindingDW2L
from pyleecan.Classes.MatLamination import MatLamination
from pyleecan.Classes.SlotW24 import SlotW24

from pyleecan.Tests import save_plot_path as save_path
from pyleecan.Tests.Plot.LamWind import wind_mat


class test_Lam_Wind_24_plot(TestCase):
    """unittest for Lamination with winding plot"""

    def test_Lam_Wind_24_wind_22(self):
        """Test machine plot with Slot 24 and winding rad=2, tan=2
        """
        print("\nTest plot Slot 24")
        plt.close("all")
        test_obj = Machine()
        test_obj.rotor = LamSlotWind(
            Rint=0.2,
            Rext=0.5,
            is_internal=True,
            is_stator=False,
            L1=0.8,
            Nrvd=4,
            Wrvd=0.05,
        )
        test_obj.rotor.slot = SlotW24(Zs=6, W3=100e-3, H2=150e-3)
        test_obj.rotor.winding = WindingUD(
            user_wind_mat=wind_mat, qs=4, p=4, Lewout=120e-3
        )
        test_obj.rotor.mat_type.mag = MatLamination(Wlam=0.5e-3)
        test_obj.shaft = Shaft(Drsh=test_obj.rotor.Rint * 2, Lshaft=1)

        test_obj.stator = LamSlotWind(
            Rint=0.51,
            Rext=0.8,
            is_internal=False,
            is_stator=True,
            L1=0.8,
            Nrvd=4,
            Wrvd=0.05,
        )
        test_obj.stator.slot = SlotW24(Zs=18, W3=50e-3, H2=200e-3)
        test_obj.stator.winding = WindingDW2L(qs=3, p=3)
        test_obj.stator.mat_type.mag = MatLamination(Wlam=0.5e-3)
        test_obj.stator.winding.Lewout = 120e-3
        test_obj.frame = Frame(Rint=0.8, Rext=0.8, Lfra=1)

        test_obj.plot()
        fig = plt.gcf()

        fig.savefig(join(save_path, "test_Lam_Wind_s24_1-Machine.png"))
        # Rotor + Stator + 0 for frame + 1 for shaft
        self.assertEqual(len(fig.axes[0].patches), 65)

        test_obj.rotor.plot()
        fig = plt.gcf()

        fig.savefig(join(save_path, "test_Lam_Wind_s24_2-Rotor.png"))
        # 2 for lam + 4*Zs for wind
        self.assertEqual(len(fig.axes[0].patches), 26)
        test_obj.stator.plot()
        fig = plt.gcf()

        fig.savefig(join(save_path, "test_Lam_Wind_s24_3-Stator.png"))
        # 2 for lam + 2*Zs for wind
        self.assertEqual(len(fig.axes[0].patches), 38)

        tooth = test_obj.rotor.slot.get_surface_tooth()
        tooth.plot(color="r")
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s24_Tooth_in.png"))

        tooth = test_obj.stator.slot.get_surface_tooth()
        tooth.plot(color="r")
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s24_Tooth_out.png"))
