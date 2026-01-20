class Dataset:
    def __init__(self, name, background_frame_ranges_list=None, clouds_frame_ranges_list=None,
                 excluded_frame_ranges_list=None, clouds_stat=None):
        self.Name = name
        self.Background_frame_ranges_list = background_frame_ranges_list
        self.Clouds_frame_ranges_list = clouds_frame_ranges_list
        self.Excluded_frame_ranges_list = excluded_frame_ranges_list
        self.Clouds_statistics = clouds_stat


cheyenne42017_07_12_night_flightship_2 = Dataset(name='cheyenne42017_07_12_night_flightship_2',
                                                 background_frame_ranges_list=[
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                     (8579, 10669)
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 7002.755675518151, "std": 474.43350428516436})

cheyenne42017_07_12_night_flightship_3 = Dataset(name='cheyenne42017_07_12_night_flightship_3',
                                                 background_frame_ranges_list=[
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                     (5704, 5704)
                                                 ],
                                                 clouds_stat={"mean": 6056.029032770793, "std": 210.5511690483262})

cheyenne42017_07_12_night_flightship_4 = Dataset(name='cheyenne42017_07_12_night_flightship_4',
                                                 background_frame_ranges_list=[
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                     (4989, 6873)
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 5894.696090198699, "std": 285.9629493271862})

cheyenne42017_07_12_night_flightship_7 = Dataset(name='cheyenne42017_07_12_night_flightship_7',
                                                 background_frame_ranges_list=[
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                     (5159, 7121)
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 5128.849130694071, "std": 324.0272423610628})

F01_D01_m47_hood_amit1_050_30_17_4_51 = Dataset(name='F01_D01_m47_hood_amit1_050_30_17_4_51',
                                                   background_frame_ranges_list=[
                                                   ],
                                                   clouds_frame_ranges_list=[
                                                       (25223, 26348)
                                                   ],
                                                   excluded_frame_ranges_list=[
                                                   ],
                                                   clouds_stat={"mean": 6960.216401290893, "std": 734.3766089984274})

F06_D05_m31_shabeyzion_hotel_090_50_18_1_41 = Dataset(name='F06_D05_m31_shabeyzion_hotel_090_50_18_1_41',
                                                      background_frame_ranges_list=[
                                                          (9417, 9477),
                                                          (9691, 9691)
                                                      ],
                                                      clouds_frame_ranges_list=[
                                                          (8178, 9372)
                                                      ],
                                                      excluded_frame_ranges_list=[
                                                          (9768, 9768)  # fog
                                                      ],
                                                      clouds_stat={"mean": 5238.187953249613, "std": 283.0217695310788})

F10_2_D02_tephen_moving_target_18_41_15 = Dataset(name='F10_2_D02_tephen_moving_target_18_41_15',
                                                  background_frame_ranges_list=[
                                                  ],
                                                  clouds_frame_ranges_list=[
                                                      (13770, 14423),
                                                      (14901, 15466)
                                                  ],
                                                  excluded_frame_ranges_list=[
                                                      (14666, 14666)  # fog
                                                  ],
                                                  clouds_stat={"mean": 6340.013825798034, "std": 287.2156328108084})

F10_4_D02_tephen_moving_target_18_45_32 = Dataset(name='F10_4_D02_tephen_moving_target_18_45_32',
                                                  background_frame_ranges_list=[
                                                      (20632, 20632)
                                                  ],
                                                  clouds_frame_ranges_list=[
                                                      (20379, 20471), #minor problem with clouds
                                                      (20938, 20981)
                                                  ],
                                                  excluded_frame_ranges_list=[
                                                      (20211, 20262),  # tags bug
                                                      (20500,20721)
                                                  ],
                                                  clouds_stat={"mean": 6308.56534650033, "std": 894.2573415744057})

F11_D12_m50_shchania_house28_090_30_18_47_14 = Dataset(name='F11_D12_m50_shchania_house28_090_30_18_47_14',
                                                       background_frame_ranges_list=[
                                                       ],
                                                       clouds_frame_ranges_list=[
                                                           (5938, 6984),
                                                           (7343, 7453)
                                                       ],
                                                       excluded_frame_ranges_list=[
                                                           (7218, 7309),  # tag ground as cloud
                                                           (7515, 7515)  # fog
                                                       ],
                                                       clouds_stat={"mean": 4877.205214691162,
                                                                    "std": 307.43142005068586})

F11_m32_poria_heli1_090_65_00442 = Dataset(name='F11_m32_poria_heli1_090_65_00442',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                           ],
                                           excluded_frame_ranges_list=[
                                               (15876, 17367)  # bad quality
                                           ],
                                           clouds_stat={"mean": 6364.53661142985, "std": 892.2635612169076})

F12_D13_m73_hadera_stop1_104_30_18_53_21 = Dataset(name='F12_D13_m73_hadera_stop1_104_30_18_53_21',
                                                   background_frame_ranges_list=[
                                                   ],
                                                   clouds_frame_ranges_list=[
                                                   ],
                                                   excluded_frame_ranges_list=[
                                                       (7839, 9067)  # fog
                                                   ],
                                                   clouds_stat={"mean": 4894.034116109212, "std": 184.19824957493387})

t01_m04a_medusa10_m1_089_50_0383 = Dataset(name='t01_m04a_medusa10_m1_089_50_0383',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                               (263778, 266774)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8245.982427300347, "std": 401.74604297407916})

t01_m05a_medusa12_m1_089_30_05a4 = Dataset(name='t01_m05a_medusa12_m1_089_30_05a4',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                               (211575, 213632)
                                           ],
                                           excluded_frame_ranges_list=[
                                               (213805, 214085)  # consider to move to background without clouds tag
                                           ],
                                           clouds_stat={"mean": 8065.049426721644, "std": 354.75973470774426})

t02_m31m_haifa01_hf011_137_60_055C = Dataset(name='t02_m31m_haifa01_hf011_137_60_055C',
                                             background_frame_ranges_list=[
                                                 # (29278, 30817)  # includ water
                                             ],
                                             clouds_frame_ranges_list=[
                                             ],
                                             excluded_frame_ranges_list=[ (29278, 30817) # excluded because it only contains water
                                             ],
                                             clouds_stat={"mean": 8040.8619669596355, "std": 164.43746976782418})

t03_m03a_medusa18_m2_005_45_0385 = Dataset(name='t03_m03a_medusa18_m2_005_45_0385',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                               (19169, 19308)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8428.125289351852, "std": 315.6864737472094})

t05_m04a_hood_amit1_69_45_02c2 = Dataset(name='t05_m04a_hood_amit1_69_45_02c2',
                                            background_frame_ranges_list=[
                                            ],
                                            clouds_frame_ranges_list=[
                                                (20563, 23025)
                                                # consider to convert to full clouds image. strange holes
                                            ],
                                            excluded_frame_ranges_list=[
                                            ],
                                            clouds_stat={"mean": 8673.80335015191, "std": 199.9824993423445})

t05_m06a_ashdod_mask2_089_30_0601 = Dataset(name='t05_m06a_ashdod_mask2_089_30_0601',
                                            background_frame_ranges_list=[
                                                (98261, 98346)
                                            ],
                                            clouds_frame_ranges_list=[
                                                (94470, 98105)
                                            ],
                                            excluded_frame_ranges_list=[
                                                (94687, 94687)
                                            ],
                                            clouds_stat={"mean": 8671.683704517505, "std": 340.4257380811352})

t05_m07a_haifa_ran11_115_45_038b = Dataset(name='t05_m07a_haifa_ran11_115_45_038b',
                                           background_frame_ranges_list=[
                                               (20567, 20567)
                                           ],
                                           clouds_frame_ranges_list=[
                                               (18336, 20567)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8469.706004503038, "std": 254.61649482605478})

t05_m10a_medusa12_m1_285_45_05a8 = Dataset(name='t05_m10a_medusa12_m1_285_45_05a8',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                               (26825, 29998)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8998.552411868248, "std": 1452.4724489826167})

t06_m01z_beitgan_ran09_300_50_02c4 = Dataset(name='t06_m01z_beit_ran09_300_50_02c4',
                                             background_frame_ranges_list=[
                                             ],
                                             clouds_frame_ranges_list=[
                                                 (263754, 266126)
                                             ],
                                             excluded_frame_ranges_list=[
                                             ],
                                             clouds_stat={"mean": 8455.435717321325, "std": 309.3361212872209})

t06_m08a_ashdod_nav2_069_60_0602 = Dataset(name='t06_m08a_ashdod_nav2_069_60_0602',
                                           background_frame_ranges_list=[
                                           ],
                                           clouds_frame_ranges_list=[
                                               (58728, 61588)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8484.189102989165, "std": 233.92052833099257})

t07_m08a_haifa_ran12_109_45_038d = Dataset(name='t07_m08a_haifa_ran12_109_45_038d',
                                           background_frame_ranges_list=[
                                               (16338, 16412)
                                           ],
                                           clouds_frame_ranges_list=[
                                               (15297, 16338),
                                               (16587, 16587)
                                           ],
                                           excluded_frame_ranges_list=[
                                           ],
                                           clouds_stat={"mean": 8441.095637568722, "std": 241.28600549476835})

t07_m10a_ashdod_urban_070_60_0603 = Dataset(name='t07_m10a_ashdod_urban_070_60_0603',
                                            background_frame_ranges_list=[
                                            ],
                                            clouds_frame_ranges_list=[
                                                (21510, 24676)
                                            ],
                                            excluded_frame_ranges_list=[
                                                (23662, 23662),
                                                (25263, 25406)
                                            ],
                                            clouds_stat={"mean": 8500.194173177084, "std": 162.7831683549563})

t09_m06a_ashdod_mask2_088_30_0605 = Dataset(name='t09_m06a_ashdod_mask2_088_30_0605',
                                            background_frame_ranges_list=[(18374, 18374)
                                            ],
                                            clouds_frame_ranges_list=[
                                                (15212, 18200)
                                            ],
                                            excluded_frame_ranges_list=[
                                            ],
                                            clouds_stat={"mean": 8554.080929000289, "std": 320.42385190435687})

t09_m07a_haifa_raan11_113_45_02c7 = Dataset(name='t09_m07a_haifa_raan11_113_45_02c7',
                                            background_frame_ranges_list=[
                                            ],
                                            clouds_frame_ranges_list=[
                                                (15581, 18027)
                                            ],
                                            excluded_frame_ranges_list=[
                                            ],
                                            clouds_stat={"mean": 8714.503876953126, "std": 327.104503770399})

t09_m19a_maapilim20_atl20_112_20_05b6 = Dataset(name='t09_m19a_maapilim20_atl20_112_20_05b6',
                                             background_frame_ranges_list=[
                                                 (23071, 26021)  # water
                                             ],
                                             clouds_frame_ranges_list=[
                                             ],
                                             excluded_frame_ranges_list=[
                                             ],
                                             clouds_stat={"mean": 8482.953910469714, "std": 129.99695282760206})

t10_m24a_naharia_bush1_085_30_05b7 = Dataset(name='t10_m24a_naharia_bush1_085_30_05b7',
                                             background_frame_ranges_list=[
                                                 (21374, 23810)  # water
                                             ],
                                             clouds_frame_ranges_list=[
                                             ],
                                             excluded_frame_ranges_list=[
                                             ],
                                             clouds_stat={"mean": 8515.490392162183, "std": 74.61562542845884})

F02_2_D11_pelech_moving_truck_17_32_10 = Dataset(name='F02_2_D11_pelech_moving_truck_17_32_10',
                                                 background_frame_ranges_list=[
                                                     (14327, 15222)  # ground
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 6512.796438697533, "std": 556.242299439608})

F02_m22_bet_ran10_040_40_00589 = Dataset(name='F02_m22_beit_ran10_040_40_00589',
                                            background_frame_ranges_list=[
                                                (10581, 12001)  # ground
                                            ],
                                            clouds_frame_ranges_list=[
                                            ],
                                            excluded_frame_ranges_list=[
                                            ],
                                            clouds_stat={"mean": 5531.26115703354, "std": 290.7585236562219})

F03_D03_m27_meron_bush1_090_85_9_35_11 = Dataset(name='F03_D03_m27_meron_bush1_090_85_9_35_11',
                                                 background_frame_ranges_list=[
                                                     (8984, 11030)  # ground
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 6472.636911957165, "std": 465.7384641771354})

F03_m55_ziron_hom3_135_20_00573_sim_release = Dataset(name='F03_m55_ziron_hom3_135_20_00573_sim_release',
                                                      background_frame_ranges_list=[
                                                          (22295, 23660)  # ground
                                                      ],
                                                      clouds_frame_ranges_list=[
                                                      ],
                                                      excluded_frame_ranges_list=[
                                                      ],
                                                      clouds_stat={"mean": 7590.801015942056, "std": 558.297544963665})

F04_m25_hood_amit1_300_30_00592 = Dataset(name='F04_m25_hood_amit1_300_30_00592',
                                             background_frame_ranges_list=[
                                                 (5994, 6964)  # ground
                                             ],
                                             clouds_frame_ranges_list=[
                                             ],
                                             excluded_frame_ranges_list=[
                                             ],
                                             clouds_stat={"mean": 5245.528154474242, "std": 151.49791172083337})

F04_m59_gal_hom1_175_30_00574 = Dataset(name='F04_m59_gal_hom1_175_30_00574',
                                        background_frame_ranges_list=[
                                            (9793, 11303)  # ground
                                        ],
                                        clouds_frame_ranges_list=[
                                        ],
                                        excluded_frame_ranges_list=[
                                        ],
                                        clouds_stat={"mean": 7618.728737011732, "std": 517.5439697846377})

F05_m27_nazarath_bsora_100_20_00594 = Dataset(name='F05_m27_nazarath_bsora_100_20_00594',
                                              background_frame_ranges_list=[
                                                  (6168, 8080)  # ground
                                              ],
                                              clouds_frame_ranges_list=[
                                              ],
                                              excluded_frame_ranges_list=[
                                              ],
                                              clouds_stat={"mean": 7618.728737011732, "std": 517.5439697846377})

F05_m52_west_hom2_050_70_00575 = Dataset(name='F05_m52_west_hom2_050_70_00575',
                                         background_frame_ranges_list=[
                                             (16856, 18469)  # ground
                                         ],
                                         clouds_frame_ranges_list=[
                                         ],
                                         excluded_frame_ranges_list=[
                                         ],
                                         clouds_stat={"mean": 7774.881730546343, "std": 490.41761034872997})

F06_D10_m85_alonmore_skali1_090_75_10_13_21 = Dataset(name='F06_D10_m85_alonmore_skali1_090_75_10_13_21',
                                                      background_frame_ranges_list=[
                                                          (11128, 12860)  # ground
                                                      ],
                                                      clouds_frame_ranges_list=[
                                                      ],
                                                      excluded_frame_ranges_list=[
                                                      ],
                                                      clouds_stat={"mean": 6299.977166316306, "std": 522.8319022012297})

F07_D07_m38_peakyou_shed1_090_20_18_9_11 = Dataset(name='F07_D07_m38_pickyou_shed1_090_20_18_9_11',
                                                 background_frame_ranges_list=[
                                                     (8240, 9800)  # ground
                                                 ],
                                                 clouds_frame_ranges_list=[
                                                 ],
                                                 excluded_frame_ranges_list=[
                                                 ],
                                                 clouds_stat={"mean": 5709.248959392024, "std": 681.3629953281702})

F08_m24_carmiel_mtsh2_250_20_00440 = Dataset(name='F08_m24_carmiel_mtsh2_250_20_00440',
                                             background_frame_ranges_list=[
                                                 (8920, 10335)  # ground
                                             ],
                                             clouds_frame_ranges_list=[
                                             ],
                                             excluded_frame_ranges_list=[(8920,10335)
                                             ],
                                             clouds_stat={"mean": 5050.309342541045, "std": 147.78640093495775})

F09_D12_m81_yosef_circle1_341_45_10_43_44 = Dataset(name='F09_D12_m81_yosef_circle1_341_45_10_43_44',
                                                     background_frame_ranges_list=[
                                                         (10537, 12520)  # ground
                                                     ],
                                                     clouds_frame_ranges_list=[
                                                     ],
                                                     excluded_frame_ranges_list=[
                                                     ],
                                                     clouds_stat={"mean": 6609.00165747885, "std": 389.7691138038733})

F09_m20_meron_iba1_090_20_00441 = Dataset(name='F09_m20_meron_iba1_090_20_00441',
                                          background_frame_ranges_list=[
                                              (6779, 8460)  # ground
                                          ],
                                          clouds_frame_ranges_list=[
                                          ],
                                          excluded_frame_ranges_list=[(6779,8460)
                                          ],
                                          clouds_stat={"mean": 4947.2722221576805, "std": 366.0701151768293})

F10_D09_m83_yosef_shemer01_155_15_10_53_45 = Dataset(name='F10_D09_m83_yosef_shemer01_155_15_10_53_45',
                                                      background_frame_ranges_list=[
                                                          (7287, 8707)  # ground
                                                      ],
                                                      clouds_frame_ranges_list=[
                                                      ],
                                                      excluded_frame_ranges_list=[
                                                      ],
                                                      clouds_stat={"mean": 6577.499669785528, "std": 342.8300623683179})

F11_D14_m88_nofaviv_rnw33w_331_10_11_0_35 = Dataset(name='F11_D14_m88_nofaviv_rnw33w_331_10_11_0_35',
                                                   background_frame_ranges_list=[
                                                       (11914, 14299)  # ground
                                                   ],
                                                   clouds_frame_ranges_list=[
                                                   ],
                                                   excluded_frame_ranges_list=[
                                                   ],
                                                   clouds_stat={"mean": 8176.650483678076, "std": 1415.5224776235773})

F14_m69_nofaviv_rnw15e_027_10_00443_wrong_33e_m66 = Dataset(name='F14_m69_nofaviv_rnw15e_027_10_00443_wrong_33e_m66',
                                                           background_frame_ranges_list=[
                                                               # (27544, 29414)  # ground
                                                           ],
                                                           clouds_frame_ranges_list=[
                                                           ],
                                                           excluded_frame_ranges_list=[(27544,29414) # bad quality
                                                           ],
                                                           clouds_stat={"mean": 6479.2850551249185,
                                                                        "std": 1006.7841672479411})

night_flight_ship_8_2017_07_12 = Dataset(name='night_flight_ship_8_2017_07_12',
                                         background_frame_ranges_list=[
                                             # (8563, 8593)  # water
                                         ],
                                         clouds_frame_ranges_list=[
                                         ],
                                         excluded_frame_ranges_list=[(8563, 8593) # excluded because it only contains water
                                         ],
                                         clouds_stat={"mean": 5537.651839846656, "std": 75.39600106775954})

night_flight_ship_10_2017_07_12 = Dataset(name='night_flight_ship_10_2017_07_12',
                                          background_frame_ranges_list=[
                                              # (5746, 6136)  # water
                                          ],
                                          clouds_frame_ranges_list=[
                                          ],
                                          excluded_frame_ranges_list=[(5746,6136) # excluded because it only contains water
                                          ],
                                          clouds_stat={"mean": 5316.011608284737, "std": 114.52969486063427})

night_flight_ship_11_2017_07_12 = Dataset(name='night_flight_ship_11_2017_07_12',
                                          background_frame_ranges_list=[
                                              # (7160, 7340)  # water
                                          ],
                                          clouds_frame_ranges_list=[
                                          ],
                                          excluded_frame_ranges_list=[(7160, 7340)   # excluded because it only contains water
                                          ],
                                          clouds_stat={"mean": 4637.7404297837265, "std": 90.17330478502694})

night_flight_ship_12_2017_07_12 = Dataset(name='night_flight_ship_12_2017_07_12',
                                          background_frame_ranges_list=[
                                              # (5750, 5875)  # water
                                          ],
                                          clouds_frame_ranges_list=[
                                          ],
                                          excluded_frame_ranges_list=[ (5750, 5875) # excluded because it only contains water
                                          ],
                                          clouds_stat={"mean": 4609.60488426991, "std": 121.94409881403823})

night_flight_ship_14_2017_07_12 = Dataset(name='night_flight_ship_14_2017_07_12',
                                          background_frame_ranges_list=[
                                              # (4676, 4696)  # water
                                          ],
                                          clouds_frame_ranges_list=[
                                          ],
                                          excluded_frame_ranges_list=[(4676, 4696) # excluded because it only contains water
                                          ],
                                          clouds_stat={"mean": 5346.826367696126, "std": 61.18493578505095})

F07_2_DS_netofa3_STPT_00302_UTC_19_32_53 = Dataset(name='F07_2_DS_netofa3_STPT_00302_UTC_19_32_53',
                                                   background_frame_ranges_list=[
                                                   ],
                                                   clouds_frame_ranges_list=[
                                                       (10895, 11126)
                                                   ],
                                                   excluded_frame_ranges_list=[
                                                   ],
                                                   clouds_stat={"mean": 6456.7501824144, "std": 60.514787796719325})

F09_m67_nofaviv_rnw33w_331_10_00304_UTC_20_10_25 = Dataset(name='F09_m67_nofaviv_rnw33w_331_10_00304_UTC_20_10_25',
                                                          background_frame_ranges_list=[
                                                          ],
                                                          clouds_frame_ranges_list=[
                                                              (17284,17304),
                                                              (17348, 23054)
                                                          ],
                                                          excluded_frame_ranges_list=[
                                                              (17209, 17281),
                                                              (17320,17320),
                                                              (17515, 17515),
                                                              (18087, 18694),
                                                              (18957, 18957),
                                                              (18999, 18999)  # wrong tag
                                                          ],
                                                          clouds_stat={"mean": 5978.423318906979,
                                                                       "std": 840.8530580041137})

jack_SqrCnt_00065 = Dataset(name='jack_SqrCnt_00065',
                             # !use for clouds only! - freestyle clouds segmentation from full clouds images
                             background_frame_ranges_list=[
                             ],
                             clouds_frame_ranges_list=[
                                 (29344, 30214)
                             ],
                             excluded_frame_ranges_list=[
                             ],
                             clouds_stat={"mean": 7166.554718271891, "std": 158.8254507403881})

jack_SqrCnt_00066 = Dataset(name='jack_SqrCnt_00066',
                             # !use for clouds only! - freestyle clouds segmentation from full clouds images
                             background_frame_ranges_list=[
                             ],
                             clouds_frame_ranges_list=[
                                 (15482, 16492)
                             ],
                             excluded_frame_ranges_list=[
                             ],
                             clouds_stat={"mean": 6663.282709916432, "std": 224.85498791840217})

jack_SqrCnt_00067 = Dataset(name='jack_SqrCnt_00067',
                             # !use for clouds only! - freestyle clouds segmentation from full clouds images
                             background_frame_ranges_list=[
                             ],
                             clouds_frame_ranges_list=[
                                 (10904, 11004)
                             ],
                             excluded_frame_ranges_list=[
                             ],
                             clouds_stat={"mean": 6266.576407877604, "std": 114.29705553087021})

#######################################################################################################
########################################### Tal yaafs #################################################
#######################################################################################################
CaptiveC8_Night_2017_05_15 = Dataset(name="CaptiveC8_Night_2017_05_15Station_3F07_3_DS_netofa3_STPT_00302_UTC_19_35_45",  # clouds
                                     background_frame_ranges_list=[(16280,16280)],
                                     clouds_frame_ranges_list=[(15520, 16260),
                                                               (16380, 16800)],
                                     excluded_frame_ranges_list=[],
                                     clouds_stat={})

cheyenne4_2017_07_12_night_flighthaifa_1 = Dataset(name="cheyenne4_2017_07_12_night_flighthaifa_1",  # clouds
                                                   background_frame_ranges_list=[],
                                                   clouds_frame_ranges_list=[(3450, 3450),
                                                                             (3590, 3590),
                                                                             (3764, 3764),
                                                                             (3915, 3915),
                                                                             (4165, 4165),
                                                                             (4340, 4340),
                                                                             (4495, 4495),
                                                                             (4665, 4665),
                                                                             (4866, 4866)],
                                                   excluded_frame_ranges_list=[(3370, 3370),  # repeats
                                                                               (3520, 3520),
                                                                               (3640, 3700),
                                                                               (3845, 3845),
                                                                               (3960, 4100),
                                                                               (4235, 4270),
                                                                               (4376, 4450),
                                                                               (4545, 4620),
                                                                               (4725, 4830),
                                                                               (4900, 4900)],
                                                   clouds_stat={})
cheyenne4_2017_07_12_night_flightjumps_1 = Dataset(name="cheyenne4_2017_07_12_night_flightjumps_1",
                                                   background_frame_ranges_list=[],
                                                   clouds_frame_ranges_list=[(4470, 4470),
                                                                             (4490, 4490),
                                                                             (4515, 4607),
                                                                             (4628, 4628),
                                                                             (4655, 5605),
                                                                             (5719, 5719),
                                                                             (5857, 5857)],
                                                   excluded_frame_ranges_list=[(4479, 4479),
                                                                               (4500, 4500),
                                                                               (4617, 4617),
                                                                               (4635, 4635),
                                                                               (5305,5305),
                                                                               (5625, 5625),
                                                                               (5765, 5765),
                                                                               (5901, 5901)],
                                                   clouds_stat={})

kashur2c_2lapid_20160504st3t03_095_20_02bf = Dataset(name="kashur2c_2lapid_north_day18_20160504st3t03_m05a_ill_hafir1_095_20_02bf",  # clouds
                                                     background_frame_ranges_list=[],
                                                     clouds_frame_ranges_list=[(16946, 16946),
                                                                               (17175, 17175),
                                                                               (17280, 17280),
                                                                               (17360, 17360),
                                                                               (17540, 17540),
                                                                               (17640, 17640),
                                                                               (17840, 17840),
                                                                               (17900, 17900),
                                                                               (18120, 18120),
                                                                               (18360, 18360),
                                                                               (18440, 18440),
                                                                               (18540, 18540),
                                                                               (18760, 18760),
                                                                               (18840, 18840),
                                                                               (19000, 19000),
                                                                               (19120, 19120)],
                                                     excluded_frame_ranges_list=[(16984, 16984),  # many repetitions
                                                                                 (17200, 17260),
                                                                                 (17300, 17340),
                                                                                 (17380, 17520),
                                                                                 (17560, 17620),
                                                                                 (17660, 17820),
                                                                                 (17860, 17880),
                                                                                 (17920, 18100),
                                                                                 (18140, 18340),
                                                                                 (18380, 18420),
                                                                                 (18460, 18520),
                                                                                 (18560, 18740),
                                                                                 (18780, 18820),
                                                                                 (18860, 18980),
                                                                                 (19020, 19100),
                                                                                 (19132, 19132)],
                                                     clouds_stat={})

kashur2c_2lapid_20160504st3t04_286_45_02c0 = Dataset(name="kashur2c_2lapid_north_day18_20160504st3t04_m06m_yishai_dtk01_286_45_02c0",  # clouds
                                                     background_frame_ranges_list=[],
                                                     clouds_frame_ranges_list=[(14960, 14960),
                                                                               (15064, 15064),
                                                                               (15138, 15138),
                                                                               (15180, 15180),
                                                                               (15340, 15340),
                                                                               (15480, 15480),
                                                                               (15680, 15680),
                                                                               (15800, 15800),
                                                                               (15860, 15860),
                                                                               (16080, 16080)],
                                                     excluded_frame_ranges_list=[(14952, 14952),
                                                                                 (14980, 15015),
                                                                                 (15089, 15113),
                                                                                 (15167, 15167),
                                                                                 (15200, 15320),
                                                                                 (15360, 15460),
                                                                                 (15500, 15660),
                                                                                 (15700, 15780),
                                                                                 (15820, 15840),
                                                                                 (15880, 16060),
                                                                                 (16100, 16125)],
                                                     clouds_stat={})

kashur2c_2lapid_20160504st3t05_69_45_02c2 = Dataset(name="kashur2c_2lapid_north_day18_20160504st3t05_m04a_sac_amit1_69_45_02c2",
                                                    background_frame_ranges_list=[],
                                                    clouds_frame_ranges_list=[(20556, 23380)],
                                                    excluded_frame_ranges_list=[(20575, 20575),
                                                                                (20620, 20655),
                                                                                (20680, 20680),
                                                                                (20705, 20743),
                                                                                (20770, 20770),
                                                                                (20820, 20960),
                                                                                (21000, 21100),
                                                                                (21140, 21240),
                                                                                (21280, 21280),
                                                                                (21320, 21320),
                                                                                (21360, 21400),
                                                                                (21440, 21500),
                                                                                (21540, 21560),
                                                                                (21600, 21620),
                                                                                (21660, 21700),
                                                                                (21740, 21780),
                                                                                (21820, 21880),
                                                                                (21920, 21980),
                                                                                (22020, 22080),
                                                                                (22120, 22160),
                                                                                (22200, 22240),
                                                                                (22280, 22300),
                                                                                (22340, 22360),
                                                                                (22400, 22460),
                                                                                (22500, 22540),
                                                                                (22580, 22640),
                                                                                (22775, 22775),
                                                                                (22820, 22820),
                                                                                (22860, 22860),
                                                                                (22900, 22900),
                                                                                (22940, 22940),
                                                                                (22980, 23020),
                                                                                (23060, 23120),
                                                                                (23160, 23160),
                                                                                (23200, 23220),
                                                                                (23260, 23260)],
                                                    clouds_stat={})

kashur2c_2lapid_20160504st3t06_300_50_02c4 = Dataset(name="kashur2c_2lapid_north_day18_20160504st3t06_m01z_beit_ran09_300_50_02c4",
                                                     background_frame_ranges_list=[],
                                                     clouds_frame_ranges_list=[(14739, 17757)],
                                                     excluded_frame_ranges_list=[(14760, 14760),
                                                                                 (14808, 14808),
                                                                                 (14846, 14858),
                                                                                 (14907, 14919),
                                                                                 (14931, 14931),
                                                                                 (14980, 14980),
                                                                                 (15020, 15060),
                                                                                 (15100, 15140),
                                                                                 (15180, 15220),
                                                                                 (15240, 15320),
                                                                                 (15340, 15340),
                                                                                 (15380, 15400),
                                                                                 (15440, 15480),
                                                                                 (15520, 15580),
                                                                                 (15620, 15640),
                                                                                 (15680, 15820),
                                                                                 (15860, 15960),
                                                                                 (16000, 16060),
                                                                                 (16100, 16160),
                                                                                 (16200, 16280),
                                                                                 (16320, 16340),
                                                                                 (16380, 16520),
                                                                                 (16580, 16660),
                                                                                 (16700, 16760),
                                                                                 (16800, 16952),
                                                                                 (16980, 17100),
                                                                                 (17140, 17220),
                                                                                 (17260, 17380),
                                                                                 (17420, 17440),
                                                                                 (17480, 17560),
                                                                                 (17600, 17600),
                                                                                 (17757, 17757)],
                                                     clouds_stat={}
                                                     )

kashur2c_2lapid_20160504st3t08_299_55_02c6 = Dataset(name="kashur2c_2lapid_north_day18_20160504st3t08_m01z_beit_ran10_299_55_02c6",
                                                     background_frame_ranges_list=[(14860, 14900)],
                                                     clouds_frame_ranges_list=[
                                                                               (13188, 16520)
                                                                               ],
                                                     excluded_frame_ranges_list=[(13188, 13271),
                                                                                 (13296, 13296),
                                                                                 (13346, 13346),
                                                                                 (13370, 13389),
                                                                                 (13420, 13440),
                                                                                 (13480, 13540),
                                                                                 (13580, 13640),
                                                                                 (13680, 13720),
                                                                                 (13760, 13800),
                                                                                 (13840, 13900),
                                                                                 (13940, 14040),
                                                                                 (14080, 14180),
                                                                                 (14220, 14340),
                                                                                 (14380, 14460),
                                                                                 (14500, 14620),
                                                                                 (14660, 14728),
                                                                                 (14760, 14840),
                                                                                 (15880, 15880),
                                                                                 (15920, 15920),
                                                                                 (16040, 16100),
                                                                                 (16140, 16220),
                                                                                 (16260, 16340),
                                                                                 (16380, 16380),
                                                                                 (16420, 16500)],
                                                     clouds_stat={}
                                                     )

kashur3c_1_20170521st3t10_090_30_05dc = Dataset(name="kashur3c_1_north_day18_20170521st3t10_m02g_shomrat_tube_090_30_05dc",
                                                background_frame_ranges_list=[],
                                                clouds_frame_ranges_list=[(30100, 30500),
                                                                          (31100, 31100),
                                                                          (31400, 31400)],
                                                excluded_frame_ranges_list=[(30600, 31000),
                                                                            (31200, 31300),
                                                                            (31500, 31600)],
                                                clouds_stat={}
                                                )

shayen3_2016_10_31_4_jumps_way_0417 = Dataset(name="shayen3_2016_10_31_ILearly_morning_flightrecording_systemt01_4_jumps_way_0417",
                                              background_frame_ranges_list=[],
                                              clouds_frame_ranges_list=[(1506,3559)],
                                          
                                              excluded_frame_ranges_list=[(1525,1625),(1675,1771), (1780,1780),
                                              (1804,1813),(1897,1906),(1922,1922),(1977,1999),
                                              (2023,2033),(2054,2109),(2133,2133),(2149,2205),
                                              (2228,2236),(2252,2252),(2293,2330),(2347,2347),
                                              (2362,2362),(2418,2440),(2457,2457),(2474,2474),
                                              (2550,2550),(2574,2574),(2590,2645),(2660,2660),
                                              (2677,2677),(2692,2692),(2714,2770),(2786,2786),
                                              (2802,2802),(2842,2880),(2896,2896),(2912,2912),
                                              (2952,2990),(3006,3006),(3022,3022),(3062,3085),
                                              (3108,3117),(3133,3133),(3210,3210),(3234,3242),
                                              (3328,3328),(3344,3344),(3360,3415),(3438,3446),
                                              (3463,3463),(3548,3559)],
                                              clouds_stat={}
                                              )
