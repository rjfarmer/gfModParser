# SPDX-License-Identifier: GPL-2.0+

import numpy as np

import gfModParser as gf


class TestUtils:
    def test_hex(self):
        assert gf.utils.hextofloat("0.12decde@9") == 5065465344.0
        assert gf.utils.hextofloat("-0.12decde@9") == -5065465344.0

    def test_hex_dble(self):
        h = gf.utils.hextofloat("0.12decde@9", kind=8)
        assert isinstance(h, np.double)

        assert h == np.double(5065465344.0)

    def test_string_clean(self):

        # fmt: off
        assert gf.utils.string_clean("'abc'") == 'abc'
        assert gf.utils.string_clean("'abc'") == 'abc'
        assert gf.utils.string_clean("abc") == 'abc'
        assert gf.utils.string_clean("") == ''
        assert gf.utils.string_clean(None) is None
        # fmt: on

    def test_hex2(self):
        assert gf.utils.hextofloat("-0.9f2d90e647ba78@-13", kind=8) == -1.380649e-16
        assert gf.utils.hextofloat("0.6f2dec549b943c@0", kind=8) == 0.43429448190325187
        assert gf.utils.hextofloat("0.c90fdaa22168c0@1", kind=8) == 12.566370614359172
        assert (
            gf.utils.hextofloat("0.d63d8fbd0746d8@15", kind=8) == 9.648533212331002e17
        )
        assert (
            gf.utils.hextofloat("-0.538d41ef94c01c@-22", kind=8)
            == -1.0545718176461565e-27
        )
        assert gf.utils.hextofloat("-0.1de3d42a1ed29d@-1", kind=8) == -0.0072973525693
        assert gf.utils.hextofloat("-0.16eb28cd34d8a1@1", kind=8) == -1.432411958301181
        assert gf.utils.hextofloat("0.15180000000000@5", kind=8) == 86400.0
        assert gf.utils.hextofloat("-0.1250d048e7a1bd@1", kind=8) == -1.1447298858494002
        assert gf.utils.hextofloat("-0.1ae14bd6bdd36b@-4", kind=8) == -1.602176634e-06
        assert gf.utils.hextofloat("0.d105eb806161f0@0", kind=8) == 0.816496580927726
        assert gf.utils.hextofloat("0.1250d048e7a1bd@1", kind=8) == 1.1447298858494002
        assert gf.utils.hextofloat("0.1c2f8fe5409db9@-9", kind=8) == 1.602176634e-12
        assert gf.utils.hextofloat("0.16a09e667f3bcc@1", kind=8) == 1.414213562373095
        assert gf.utils.hextofloat("-0.20cf8ab396a2d8@-21", kind=8) == -6.62607015e-27
        assert gf.utils.hextofloat("-0.b17217f7d1cf78@0", kind=8) == -0.6931471805599453
        assert gf.utils.hextofloat("0.9f2d90e647ba78@-13", kind=8) == 1.380649e-16
        assert gf.utils.hextofloat("-0.4f4afb22e78e84@7", kind=8) == -83144626.1815324
        assert (
            gf.utils.hextofloat("0.201e97585f60bc@-19", kind=8)
            == 1.6605390671738466e-24
        )
        assert gf.utils.hextofloat("0.482c067009be74@-22", kind=8) == 9.1093837015e-28
        assert gf.utils.hextofloat("-0.1193ea7aad030a@1", kind=8) == -1.0986122886681096
        assert gf.utils.hextofloat("0.205a6c2f7e45e8@-19", kind=8) == 1.67262192369e-24
        assert gf.utils.hextofloat("-0.30000000000000@1", kind=8) == -3.0
        assert gf.utils.hextofloat("0.2212b251e94952@-11", kind=8) == 7.56573325028e-15
        assert (
            gf.utils.hextofloat("-0.2101e3186a4558@-7", kind=8)
            == -4.803204712570263e-10
        )
        assert gf.utils.hextofloat("0.cde235499f1d50@-20", kind=8) == 6.6524587321e-25
        assert (
            gf.utils.hextofloat("0.3b754ba13ce6d8@-3", kind=8) == 5.670374419184426e-05
        )
        assert gf.utils.hextofloat("-0.394bb834c783f0@2", kind=8) == -57.29577951308232
        assert gf.utils.hextofloat("-0.1aaaaaaaaaaaab@1", kind=8) == -1.6666666666666667
        assert gf.utils.hextofloat("-0.9de9e64df22ef0@1", kind=8) == -9.869604401089358
        assert gf.utils.hextofloat("8", kind=8) == 8
        assert (
            gf.utils.hextofloat("-0.d21206c8963a30@15", kind=8) == -9.4607304725808e17
        )
        assert gf.utils.hextofloat("-0.390ff972474538@0", kind=8) == -0.2229
        assert (
            gf.utils.hextofloat("-0.8d3cade53f5e98@-22", kind=8)
            == -1.7826619216278976e-27
        )
        assert (
            gf.utils.hextofloat("-0.d63d8fbd0746e0@15", kind=8) == -9.648533212331003e17
        )
        assert gf.utils.hextofloat("0.7f8617295f145c@20", kind=8) == 6.02214076e23
        assert gf.utils.hextofloat("-0.1e187e00000000@7", kind=8) == -31557600.0
        assert gf.utils.hextofloat("0.9f2d90e647ba78@-13", kind=8) == 1.380649e-16
        assert gf.utils.hextofloat("-0.1c2f8fe5409db9@-9", kind=8) == -1.602176634e-12
        assert gf.utils.hextofloat("-0.430548e0b5cd94@1", kind=8) == -4.1887902047863905
        assert gf.utils.hextofloat("0.2065d6d9258c0c@-19", kind=8) == 1.67492749804e-24
        assert gf.utils.hextofloat("-0.55555555555554@0", kind=8) == -0.3333333333333333
        assert gf.utils.hextofloat("-0.3243f6a8885a30@1", kind=8) == -3.141592653589793
        assert gf.utils.hextofloat("0.d9b0eb45aabdc8@1", kind=8) == 13.605693122994
        assert gf.utils.hextofloat("0.4f4afb22e78e84@7", kind=8) == 83144626.1815324
        assert gf.utils.hextofloat("-0.16a09e667f3bcc@1", kind=8) == -1.414213562373095
        assert gf.utils.hextofloat("0.aaaaaaaaaaaaa8@0", kind=8) == 0.6666666666666666
        assert gf.utils.hextofloat("0.55555555555554@0", kind=8) == 0.3333333333333333
        assert gf.utils.hextofloat("0.16ba5d6e5fabb0@-6", kind=8) == 5.29177210903e-09
        assert (
            gf.utils.hextofloat("0.2101e3186a4558@-7", kind=8) == 4.803204712570263e-10
        )
        assert (
            gf.utils.hextofloat("0.8d3cade53f5e98@-22", kind=8)
            == 1.7826619216278976e-27
        )
        assert (
            gf.utils.hextofloat("-0.5a5bfa538b3e78@-3", kind=8)
            == -8.617333262145177e-05
        )
        assert (
            gf.utils.hextofloat("0.5a5bfa538b3e78@-3", kind=8) == 8.617333262145177e-05
        )
        assert gf.utils.hextofloat("0.1e187e00000000@7", kind=8) == 31557600.0
        assert gf.utils.hextofloat("-0.16ba5d6e5fabb0@-6", kind=8) == -5.29177210903e-09
        assert gf.utils.hextofloat("-0.93c467e37db0c8@0", kind=8) == -0.5772156649015329
        assert gf.utils.hextofloat("-0.24d763776aaa2a@1", kind=8) == -2.3025850929940455
        assert gf.utils.hextofloat("0.20cf8ab396a2d8@-21", kind=8) == 6.62607015e-27
        assert gf.utils.hextofloat("-0.7f8617295f145c@20", kind=8) == -6.02214076e23
        assert gf.utils.hextofloat("-0.d9b0eb45aabdc8@1", kind=8) == -13.605693122994
        assert gf.utils.hextofloat("0.1193ea7aad030a@1", kind=8) == 1.0986122886681096
        assert gf.utils.hextofloat("-0.9f2d90e647ba78@-13", kind=8) == -1.380649e-16
        assert gf.utils.hextofloat("0.390ff972474538@0", kind=8) == 0.2229
        assert gf.utils.hextofloat("0.1965fea53d6e3c@1", kind=8) == 1.5874010519681994
        assert gf.utils.hextofloat("0.2aaaaaaaaaaaaa@0", kind=8) == 0.16666666666666666
        assert gf.utils.hextofloat("0.394bb834c783f0@2", kind=8) == 57.29577951308232
        assert gf.utils.hextofloat("0.d9b18cb5230000@11", kind=8) == 14959787070000.0
        assert gf.utils.hextofloat("0.1de3d42a1ed29d@-1", kind=8) == 0.0072973525693
        assert gf.utils.hextofloat("0.430548e0b5cd94@1", kind=8) == 4.1887902047863905
        assert gf.utils.hextofloat("0.2b7e151628aed2@1", kind=8) == 2.718281828459045
        assert gf.utils.hextofloat("0.3243f6a8885a30@1", kind=8) == 3.141592653589793
        assert (
            gf.utils.hextofloat("-0.3b754ba13ce6d8@-3", kind=8)
            == -5.670374419184426e-05
        )
        assert gf.utils.hextofloat("0.1428a2f98d728a@1", kind=8) == 1.259921049894873
        assert (
            gf.utils.hextofloat("-0.201e97585f60bc@-19", kind=8)
            == -1.6605390671738466e-24
        )
        assert gf.utils.hextofloat("0.24d763776aaa2a@1", kind=8) == 2.3025850929940455
        assert gf.utils.hextofloat("0.9de9e64df22ef0@1", kind=8) == 9.869604401089358
        assert (
            gf.utils.hextofloat("-0.477d1a894a74e4@-1", kind=8) == -0.017453292519943295
        )
        assert gf.utils.hextofloat("0.30000000000000@1", kind=8) == 3.0
        assert gf.utils.hextofloat("0.15555555555555@1", kind=8) == 1.3333333333333333
        assert gf.utils.hextofloat("0.1ae14bd6bdd36b@-4", kind=8) == 1.602176634e-06
        assert (
            gf.utils.hextofloat("-0.d63d8fbd0746d8@15", kind=8) == -9.648533212331002e17
        )
        assert (
            gf.utils.hextofloat("-0.205a6c2f7e45e8@-19", kind=8) == -1.67262192369e-24
        )
        assert gf.utils.hextofloat("0.1aaaaaaaaaaaab@1", kind=8) == 1.6666666666666667
        assert gf.utils.hextofloat("0.16d40000000000@3", kind=8) == 365.25
        assert gf.utils.hextofloat("0.93c467e37db0c8@0", kind=8) == 0.5772156649015329
        assert gf.utils.hextofloat("-0.aaaaaaaaaaaaa8@0", kind=8) == -0.6666666666666666
        assert gf.utils.hextofloat("0.6fae6fce800000@9", kind=8) == 29979245800.0
        assert gf.utils.hextofloat("-0.2b7e151628aed2@1", kind=8) == -2.718281828459045
        assert (
            gf.utils.hextofloat("-0.2212b251e94952@-11", kind=8) == -7.56573325028e-15
        )
        assert gf.utils.hextofloat("-0.1428a2f98d728a@1", kind=8) == -1.259921049894873
        assert gf.utils.hextofloat("-0.16d40000000000@3", kind=8) == -365.25
        assert (
            gf.utils.hextofloat("-0.2065d6d9258c0c@-19", kind=8) == -1.67492749804e-24
        )
        assert gf.utils.hextofloat("-0.6fae6fce800000@9", kind=8) == -29979245800.0
        assert (
            gf.utils.hextofloat("0.477d1a894a74e4@-1", kind=8) == 0.017453292519943295
        )
        assert gf.utils.hextofloat("-0.15555555555555@1", kind=8) == -1.3333333333333333
        assert (
            gf.utils.hextofloat("-0.2ad28769682dee@16", kind=8)
            == -3.0856775814913674e18
        )
        assert (
            gf.utils.hextofloat("0.2ad28769682dee@16", kind=8) == 3.0856775814913674e18
        )
        assert gf.utils.hextofloat("-0.c90fdaa22168c0@1", kind=8) == -12.566370614359172
        assert (
            gf.utils.hextofloat("0.d63d8fbd0746e0@15", kind=8) == 9.648533212331003e17
        )
        assert (
            gf.utils.hextofloat("-0.2aaaaaaaaaaaaa@0", kind=8) == -0.16666666666666666
        )
        assert gf.utils.hextofloat("-0.cde235499f1d50@-20", kind=8) == -6.6524587321e-25
        assert gf.utils.hextofloat("-0.15180000000000@5", kind=8) == -86400.0
        assert (
            gf.utils.hextofloat("-0.6f2dec549b943c@0", kind=8) == -0.43429448190325187
        )
        assert gf.utils.hextofloat("0.b17217f7d1cf78@0", kind=8) == 0.6931471805599453
        assert gf.utils.hextofloat("0.d21206c8963a30@15", kind=8) == 9.4607304725808e17
        assert gf.utils.hextofloat("-0.482c067009be74@-22", kind=8) == -9.1093837015e-28
        assert (
            gf.utils.hextofloat("0.538d41ef94c01c@-22", kind=8)
            == 1.0545718176461565e-27
        )
        assert gf.utils.hextofloat("-0.d9b18cb5230000@11", kind=8) == -14959787070000.0
        assert gf.utils.hextofloat("0.16eb28cd34d8a1@1", kind=8) == 1.432411958301181
        assert gf.utils.hextofloat("-0.d105eb806161f0@0", kind=8) == -0.816496580927726
        assert gf.utils.hextofloat("-0.1965fea53d6e3c@1", kind=8) == -1.5874010519681994
