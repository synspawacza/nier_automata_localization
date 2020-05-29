#!/bin/bash

#empty LANG2 and LANG3 are for jp
LANG2="_us" # _fr _it _de _es
LANG3="_eng" # _fra _ita _ger _esp
TLANG="_pl" # language suffix from 

function put_strings() {
    DAT_FILE=${1}
    NAME=${2}
    EXT=${3}
    echo "building ${NAME}"
    
    if [[ ${EXT} == "txt" ]]; then
        mkdir -p output/novel
        cp target/${NAME}.${EXT} output/novel/${NAME}.${EXT}
    elif [[ ${EXT} == "mcd" ]]; then
        DTT_FILE=${DAT_FILE/.dat/.dtt}
        mkdir -p assembly/${DAT_FILE}/
        mkdir -p assembly/${DTT_FILE}/
        ./tools/put_strings_mcd.py unpacked/${DAT_FILE}/${NAME}.mcd target/${NAME}${TLANG}.properties fonts/fonts.json assembly/${DAT_FILE}/${NAME}.mcd assembly/${DTT_FILE}/${NAME}.wtp_000.png
        convert -define dds:mipmaps=0 assembly/${DTT_FILE}/${NAME}.wtp_000.png assembly/${DTT_FILE}/${NAME}.wtp_000.dds
        ./tools/repack_wtp.py unpacked/${DAT_FILE}/${NAME}.wta unpacked/${DTT_FILE}/${NAME}.wtp assembly/${DAT_FILE}/${NAME}.wta assembly/${DTT_FILE}/${NAME}.wtp --texture 0 assembly/${DTT_FILE}/${NAME}.wtp_000.dds
        mkdir -p `dirname output/${DAT_FILE}`
        mkdir -p `dirname output/${DTT_FILE}`
        ./tools/repack_dat.py data/${DAT_FILE} output/${DAT_FILE} assembly/${DAT_FILE}/*
        ./tools/repack_dat.py data/${DTT_FILE} output/${DTT_FILE} assembly/${DTT_FILE}/${NAME}.wtp
    else
        mkdir -p assembly/${DAT_FILE}/
        ./tools/put_strings.py unpacked/${DAT_FILE}/${NAME}.${EXT} target/${NAME}${TLANG}.properties assembly/${DAT_FILE}/${NAME}.${EXT}
        if [[ ${EXT} == "tmd" ||  ${EXT} == "smd" ]];  then
            mkdir -p `dirname output/${DAT_FILE}`
            ./tools/repack_dat.py data/${DAT_FILE} output/${DAT_FILE} assembly/${DAT_FILE}/${NAME}.${EXT}
        fi
    fi
    
}

function repack_dat() {
    mkdir -p `dirname output/${1}`
    ./tools/repack_dat.py data/${1} output/${1} assembly/${1}/*
}

put_strings core/corehap.dat global_d595bcd1_scp bin
put_strings core/corehap.dat global_60efb803_scp bin
put_strings core/corehap.dat global_638e40c8_scp bin
put_strings core/corehap.dat core_hap pak; repack_dat core/corehap.dat
put_strings ph1/p100.dat p100_fa238e7c_scp bin
put_strings ph1/p100.dat p100_c6ab1d8f_scp bin
put_strings ph1/p100.dat p100_dfcc155d_scp bin
put_strings ph1/p100.dat p100_7f31f924_scp bin
put_strings ph1/p100.dat p100_d8a4a747_scp bin
put_strings ph1/p100.dat p100_e1dc4db4_scp bin
put_strings ph1/p100.dat p100_e2d39d13_scp bin
put_strings ph1/p100.dat p100_440fda42_scp bin
put_strings ph1/p100.dat p100_536bd4fb_scp bin
put_strings ph1/p100.dat p100_7c282dc8_scp bin
put_strings ph1/p100.dat p100_cbfd7706_scp bin
put_strings ph1/p100.dat p100_6a34d49e_scp bin
put_strings ph1/p100.dat p100_301b50d3_scp bin
put_strings ph1/p100.dat p100_5f2b7c58_scp bin
put_strings ph1/p100.dat p100_a85f65ec_scp bin
put_strings ph1/p100.dat p100_10a1b8c_scp bin
put_strings ph1/p100.dat p100_8371cfcf_scp bin
put_strings ph1/p100.dat p100_54edd5c_scp bin
put_strings ph1/p100.dat p100_ce928ad9_scp bin
put_strings ph1/p100.dat p100_89910ddf_scp bin
put_strings ph1/p100.dat p100_a5817204_scp bin
put_strings ph1/p100.dat p100_6695192d_scp bin
put_strings ph1/p100.dat p100_4aa7dace_scp bin
put_strings ph1/p100.dat p100_43f203b8_scp bin
put_strings ph1/p100.dat p100_90998b13_scp bin
put_strings ph1/p100.dat p100_973474b4_scp bin
put_strings ph1/p100.dat p100_69ab2de6_scp bin
put_strings ph1/p100.dat p100_643b9449_scp bin
put_strings ph1/p100.dat p100_306867fd_scp bin
put_strings ph1/p100.dat p100_61b598fd_scp bin
put_strings ph1/p100.dat p100_39cda07a_scp bin
put_strings ph1/p100.dat p100_9092a1f1_scp bin
put_strings ph1/p100.dat p100_1a401b0f_scp bin
put_strings ph1/p100.dat p100_ec82f9bf_scp bin
put_strings ph1/p100.dat p100_cb2621f3_scp bin
put_strings ph1/p100.dat p100_56f39801_scp bin
put_strings ph1/p100.dat p100_6fc2accc_scp bin
put_strings ph1/p100.dat p100_824dfa10_scp bin
put_strings ph1/p100.dat p100_508c029e_scp bin
put_strings ph1/p100.dat p100_a2a7da53_scp bin
put_strings ph1/p100.dat p100_23622eee_scp bin
put_strings ph1/p100.dat p100_56e518db_scp bin
put_strings ph1/p100.dat p100_2299a056_scp bin
put_strings ph1/p100.dat p100_73ce9cac_scp bin
put_strings ph1/p100.dat p100_adc09aec_scp bin
put_strings ph1/p100.dat p100_81c8f672_scp bin
put_strings ph1/p100.dat p100_47a5d6eb_scp bin
put_strings ph1/p100.dat p100_9b15340d_scp bin
put_strings ph1/p100.dat p100_264b174c_scp bin; repack_dat ph1/p100.dat
put_strings ph2/p200.dat p200_a2a7da53_scp bin
put_strings ph2/p200.dat p200_2e8bdcb0_scp bin
put_strings ph2/p200.dat p200_886c2178_scp bin
put_strings ph2/p200.dat p200_92dddd6e_scp bin
put_strings ph2/p200.dat p200_bb51fdfc_scp bin
put_strings ph2/p200.dat p200_b99094bd_scp bin
put_strings ph2/p200.dat p200_20084f1f_scp bin
put_strings ph2/p200.dat p200_a3d6d2f5_scp bin
put_strings ph2/p200.dat p200_7c0c6f18_scp bin
put_strings ph2/p200.dat p200_c544d6ad_scp bin
put_strings ph2/p200.dat p200_78334de1_scp bin
put_strings ph2/p200.dat p200_24125524_scp bin
put_strings ph2/p200.dat p200_7398bbfd_scp bin
put_strings ph2/p200.dat p200_24194e13_scp bin
put_strings ph2/p200.dat p200_647d1cd7_scp bin
put_strings ph2/p200.dat p200_3c562f91_scp bin
put_strings ph2/p200.dat p200_ff3d446f_scp bin
put_strings ph2/p200.dat p200_d0b71b3b_scp bin
put_strings ph2/p200.dat p200_71c59d9f_scp bin
put_strings ph2/p200.dat p200_8cbb3f1e_scp bin
put_strings ph2/p200.dat p200_2bfce9ed_scp bin
put_strings ph2/p200.dat p200_48a7f0fd_scp bin
put_strings ph2/p200.dat p200_6ae550e0_scp bin
put_strings ph2/p200.dat p200_96e13a06_scp bin
put_strings ph2/p200.dat p200_ad4026af_scp bin
put_strings ph2/p200.dat p200_8182a35a_scp bin
put_strings ph2/p200.dat p200_27db07bb_scp bin
put_strings ph2/p200.dat p200_20cd934d_scp bin
put_strings ph2/p200.dat p200_5dfcaace_scp bin
put_strings ph2/p200.dat p200_e723b449_scp bin
put_strings ph2/p200.dat p200_a1e11071_scp bin
put_strings ph2/p200.dat p200_e8fce7cc_scp bin
put_strings ph2/p200.dat p200_4b245f40_scp bin
put_strings ph2/p200.dat p200_c7ba8911_scp bin
put_strings ph2/p200.dat p200_f764463b_scp bin
put_strings ph2/p200.dat p200_a68c4ea9_scp bin
put_strings ph2/p200.dat p200_e8cf2a5c_scp bin
put_strings ph2/p200.dat p200_58623dde_scp bin
put_strings ph2/p200.dat p200_d5ac1e7d_scp bin
put_strings ph2/p200.dat p200_1cc100aa_scp bin
put_strings ph2/p200.dat p200_398cde2c_scp bin
put_strings ph2/p200.dat p200_f1f22ca2_scp bin
put_strings ph2/p200.dat p200_aad478cc_scp bin
put_strings ph2/p200.dat p200_7914bf_scp bin
put_strings ph2/p200.dat p200_c44b75b3_scp bin
put_strings ph2/p200.dat p200_b4fc12d6_scp bin
put_strings ph2/p200.dat p200_1fcb850d_scp bin
put_strings ph2/p200.dat p200_67909aeb_scp bin
put_strings ph2/p200.dat p200_8806bcb7_scp bin
put_strings ph2/p200.dat p200_7793b6d6_scp bin
put_strings ph2/p200.dat p200_17d05835_scp bin
put_strings ph2/p200.dat p200_99454795_scp bin
put_strings ph2/p200.dat p200_56645a4b_scp bin
put_strings ph2/p200.dat p200_9a8a8724_scp bin
put_strings ph2/p200.dat p200_8767f81e_scp bin
put_strings ph2/p200.dat p200_40b3c93d_scp bin
put_strings ph2/p200.dat p200_c3ab84c7_scp bin
put_strings ph2/p200.dat p200_d0a7f4dc_scp bin
put_strings ph2/p200.dat p200_cc694d55_scp bin
put_strings ph2/p200.dat p200_7a5876f7_scp bin
put_strings ph2/p200.dat p200_d75fa9d2_scp bin
put_strings ph2/p200.dat p200_dad50fa7_scp bin
put_strings ph2/p200.dat p200_9dd3606e_scp bin
put_strings ph2/p200.dat p200_6aa3f28e_scp bin
put_strings ph2/p200.dat p200_2311697b_scp bin
put_strings ph2/p200.dat p200_1de99b24_scp bin
put_strings ph2/p200.dat p200_3456f87_scp bin
put_strings ph2/p200.dat p200_8118914c_scp bin
put_strings ph2/p200.dat p200_5a63902e_scp bin
put_strings ph2/p200.dat p200_2fb68036_scp bin; repack_dat ph2/p200.dat
put_strings ph3/p300.dat p300_f80fe22d_scp bin
put_strings ph3/p300.dat p300_abb1d768_scp bin
put_strings ph3/p300.dat p300_69ab2de6_scp bin
put_strings ph3/p300.dat p300_fe415e44_scp bin
put_strings ph3/p300.dat p300_e9106cc6_scp bin
put_strings ph3/p300.dat p300_a60ff1fc_scp bin
put_strings ph3/p300.dat p300_d578eca9_scp bin
put_strings ph3/p300.dat p300_26ad4903_scp bin
put_strings ph3/p300.dat p300_8352dd61_scp bin
put_strings ph3/p300.dat p300_1cc46857_scp bin
put_strings ph3/p300.dat p300_a34d9d8a_scp bin
put_strings ph3/p300.dat p300_2ac25a34_scp bin
put_strings ph3/p300.dat p300_e47baab_scp bin
put_strings ph3/p300.dat p300_73ee82d4_scp bin
put_strings ph3/p300.dat p300_1c94bbb3_scp bin
put_strings ph3/p300.dat p300_969b4cd4_scp bin
put_strings ph3/p300.dat p300_52095a27_scp bin
put_strings ph3/p300.dat p300_5f56e621_scp bin
put_strings ph3/p300.dat p300_d7fb6a72_scp bin
put_strings ph3/p300.dat p300_a80afa1d_scp bin
put_strings ph3/p300.dat p300_58e3f469_scp bin
put_strings ph3/p300.dat p300_b863f435_scp bin
put_strings ph3/p300.dat p300_4ac43a7f_scp bin
put_strings ph3/p300.dat p300_f29af5ee_scp bin
put_strings ph3/p300.dat p300_59a32047_scp bin
put_strings ph3/p300.dat p300_ebb2aa60_scp bin
put_strings ph3/p300.dat p300_2b0332c8_scp bin
put_strings ph3/p300.dat p300_8f18b72c_scp bin
put_strings ph3/p300.dat p300_78ebd792_scp bin
put_strings ph3/p300.dat p300_4fce2323_scp bin
put_strings ph3/p300.dat p300_abb0feab_scp bin
put_strings ph3/p300.dat p300_7677d46d_scp bin
put_strings ph3/p300.dat p300_33eec348_scp bin
put_strings ph3/p300.dat p300_312ca323_scp bin
put_strings ph3/p300.dat p300_b01535dd_scp bin
put_strings ph3/p300.dat p300_6f88066d_scp bin
put_strings ph3/p300.dat p300_454d3c27_scp bin
put_strings ph3/p300.dat p300_fb6b9581_scp bin
put_strings ph3/p300.dat p300_838131a5_scp bin
put_strings ph3/p300.dat p300_540e0da_scp bin
put_strings ph3/p300.dat p300_e3d05ab7_scp bin
put_strings ph3/p300.dat p300_dd8b37bd_scp bin
put_strings ph3/p300.dat p300_9d8df164_scp bin
put_strings ph3/p300.dat p300_af5fb37c_scp bin
put_strings ph3/p300.dat p300_d48627b4_scp bin
put_strings ph3/p300.dat p300_34ffac43_scp bin
put_strings ph3/p300.dat p300_2460bab4_scp bin
put_strings ph3/p300.dat p300_fe580523_scp bin
put_strings ph3/p300.dat p300_be18477d_scp bin
put_strings ph3/p300.dat p300_7220e53d_scp bin
put_strings ph3/p300.dat p300_79a7d0d0_scp bin
put_strings ph3/p300.dat p300_cc42e29e_scp bin
put_strings ph3/p300.dat p300_d86d80b1_scp bin
put_strings ph3/p300.dat p300_fb5ab100_scp bin
put_strings ph3/p300.dat p300_62973173_scp bin
put_strings ph3/p300.dat p300_249dcf6a_scp bin
put_strings ph3/p300.dat p300_f0e6bd59_scp bin
put_strings ph3/p300.dat p300_95a183ba_scp bin
put_strings ph3/p300.dat p300_24fd47f4_scp bin
put_strings ph3/p300.dat p300_50eb25b8_scp bin
put_strings ph3/p300.dat p300_ac91bbe4_scp bin
put_strings ph3/p300.dat p300_d913dcc1_scp bin
put_strings ph3/p300.dat p300_df90c81a_scp bin
put_strings ph3/p300.dat p300_54b1765c_scp bin
put_strings ph3/p300.dat p300_9b77492c_scp bin
put_strings ph3/p300.dat p300_4a0a3acc_scp bin
put_strings ph3/p300.dat p300_157c0c19_scp bin
put_strings ph3/p300.dat p300_802d17e9_scp bin
put_strings ph3/p300.dat p300_fca61b8d_scp bin
put_strings ph3/p300.dat p300_544f9315_scp bin
put_strings ph3/p300.dat p300_987be645_scp bin
put_strings ph3/p300.dat p300_68b9c234_scp bin
put_strings ph3/p300.dat p300_10112854_scp bin
put_strings ph3/p300.dat p300_d2ca712b_scp bin
put_strings ph3/p300.dat p300_7de5c329_scp bin
put_strings ph3/p300.dat p300_f4f38872_scp bin
put_strings ph3/p300.dat p300_4716685f_scp bin
put_strings ph3/p300.dat p300_e6cf440a_scp bin
put_strings ph3/p300.dat p300_22633b31_scp bin
put_strings ph3/p300.dat p300_ae2eada6_scp bin
put_strings ph3/p300.dat p300_d2de713_scp bin
put_strings ph3/p300.dat p300_c0c1e86c_scp bin
put_strings ph3/p300.dat p300_e4c7a829_scp bin; repack_dat ph3/p300.dat
put_strings ph4/p400.dat p400_b0e38442_scp bin
put_strings ph4/p400.dat p400_fc21ced3_scp bin
put_strings ph4/p400.dat p400_3af366c3_scp bin
put_strings ph4/p400.dat p400_5b4661f4_scp bin
put_strings ph4/p400.dat p400_42374ea5_scp bin
put_strings ph4/p400.dat p400_1afc5db6_scp bin
put_strings ph4/p400.dat p400_5489214b_scp bin; repack_dat ph4/p400.dat
put_strings phf/pf10.dat pf10_7de5c329_scp bin; repack_dat phf/pf10.dat
put_strings phf/pf30.dat pf30_148bec7a_scp bin; repack_dat phf/pf30.dat
put_strings phf/pf31.dat pf31_d2ca712b_scp bin; repack_dat phf/pf31.dat
put_strings phf/pf60.dat pf60_149e7cbe_scp bin; repack_dat phf/pf60.dat
put_strings quest/q020.dat q020_404eba3d_scp bin; repack_dat quest/q020.dat
put_strings quest/q031.dat q031_b551328a_scp bin; repack_dat quest/q031.dat
put_strings quest/q032.dat q032_94bdfeb7_scp bin; repack_dat quest/q032.dat
put_strings quest/q040.dat q040_cf7c14d9_scp bin; repack_dat quest/q040.dat
put_strings quest/q070.dat q070_fb360535_scp bin; repack_dat quest/q070.dat
put_strings quest/q071.dat q071_1a17171a_scp bin; repack_dat quest/q071.dat
put_strings quest/q080.dat q080_64afc72a_scp bin; repack_dat quest/q080.dat
put_strings quest/q090.dat q090_11b12a94_scp bin
put_strings quest/q090.dat q090_86062922_scp bin
put_strings quest/q090.dat q090_105d4edd_scp bin; repack_dat quest/q090.dat
put_strings quest/q091.dat q091_def6c866_scp bin
put_strings quest/q091.dat q091_402dfd2e_scp bin
put_strings quest/q091.dat q091_e03615dd_scp bin
put_strings quest/q091.dat q091_2f2a0eea_scp bin; repack_dat quest/q091.dat
put_strings quest/q092.dat q092_3cd7f934_scp bin
put_strings quest/q092.dat q092_35330df_scp bin
put_strings quest/q092.dat q092_82c2e878_scp bin; repack_dat quest/q092.dat
put_strings quest/q095.dat q095_fc4d3b85_scp bin; repack_dat quest/q095.dat
put_strings quest/q100.dat q100_f4f7e973_scp bin; repack_dat quest/q100.dat
put_strings quest/q101.dat q101_5be5b4cc_scp bin; repack_dat quest/q101.dat
put_strings quest/q102.dat q102_28e223f7_scp bin; repack_dat quest/q102.dat
put_strings quest/q103.dat q103_d2b3f5a6_scp bin; repack_dat quest/q103.dat
put_strings quest/q104.dat q104_e9ff21ee_scp bin; repack_dat quest/q104.dat
put_strings quest/q110.dat q110_171236f0_scp bin; repack_dat quest/q110.dat
put_strings quest/q120.dat q120_8dcd7a1a_scp bin; repack_dat quest/q120.dat
put_strings quest/q121.dat q121_70545c1f_scp bin; repack_dat quest/q121.dat
put_strings quest/q122.dat q122_3a5128c8_scp bin; repack_dat quest/q122.dat
put_strings quest/q123.dat q123_6fde04e_scp bin; repack_dat quest/q123.dat
put_strings quest/q130.dat q130_b68bfe22_scp bin; repack_dat quest/q130.dat
put_strings quest/q140.dat q140_7cda31e_scp bin; repack_dat quest/q140.dat
put_strings quest/q150.dat q150_d31e5833_scp bin; repack_dat quest/q150.dat
put_strings quest/q160.dat q160_d8b9d0be_scp bin; repack_dat quest/q160.dat
put_strings quest/q162.dat q162_fc7da4a2_scp bin; repack_dat quest/q162.dat
put_strings quest/q170.dat q170_96333b78_scp bin; repack_dat quest/q170.dat
put_strings quest/q171.dat q171_12f2963a_scp bin; repack_dat quest/q171.dat
put_strings quest/q180.dat q180_2d2126d2_scp bin; repack_dat quest/q180.dat
put_strings quest/q181.dat q181_746d944f_scp bin; repack_dat quest/q181.dat
put_strings quest/q210.dat q210_a6306d6c_scp bin; repack_dat quest/q210.dat
put_strings quest/q220.dat q220_e880784a_scp bin; repack_dat quest/q220.dat
put_strings quest/q221.dat q221_b113244a_scp bin; repack_dat quest/q221.dat
put_strings quest/q222.dat q222_f8217e42_scp bin; repack_dat quest/q222.dat
put_strings quest/q290.dat q290_e15f2fa1_scp bin; repack_dat quest/q290.dat
put_strings quest/q300.dat q300_5f9ed04e_scp bin; repack_dat quest/q300.dat
put_strings quest/q330.dat q330_21f485e_scp bin
put_strings quest/q330.dat q330_70a701da_scp bin
put_strings quest/q330.dat q330_9bafd382_scp bin
put_strings quest/q330.dat q330_b853020f_scp bin
put_strings quest/q330.dat q330_ee317264_scp bin; repack_dat quest/q330.dat
put_strings quest/q340.dat q340_5620eb59_scp bin; repack_dat quest/q340.dat
put_strings quest/q360.dat q360_8efed5ef_scp bin; repack_dat quest/q360.dat
put_strings quest/q400.dat q400_1f6199eb_scp bin
put_strings quest/q400.dat q400_21ca35cb_scp bin
put_strings quest/q400.dat q400_48d76c20_scp bin
put_strings quest/q400.dat q400_fc5b48ad_scp bin; repack_dat quest/q400.dat
put_strings quest/q401.dat q401_643e5418_scp bin; repack_dat quest/q401.dat
put_strings quest/q403.dat q403_5d43ba8b_scp bin; repack_dat quest/q403.dat
put_strings quest/q410.dat q410_4f2b901a_scp bin; repack_dat quest/q410.dat
put_strings quest/q440.dat q440_3b4ef61d_scp bin; repack_dat quest/q440.dat
put_strings quest/q500.dat q500_8446c06e_scp bin; repack_dat quest/q500.dat
put_strings quest/q520.dat q520_afd5aa67_scp bin; repack_dat quest/q520.dat
put_strings quest/q532.dat q532_65ff89bf_scp bin; repack_dat quest/q532.dat
put_strings quest/q540.dat q540_e1207097_scp bin; repack_dat quest/q540.dat
put_strings quest/q550.dat q550_688e8050_scp bin; repack_dat quest/q550.dat
put_strings quest/q560.dat q560_291dbe71_scp bin; repack_dat quest/q560.dat
put_strings quest/q561.dat q561_74b9a716_scp bin; repack_dat quest/q561.dat
put_strings quest/q562.dat q562_e10ec9ab_scp bin; repack_dat quest/q562.dat
put_strings quest/q590.dat q590_13ffe891_scp bin; repack_dat quest/q590.dat
put_strings quest/q640.dat q640_ccd60068_scp bin; repack_dat quest/q640.dat
put_strings quest/q650.dat q650_96497077_scp bin; repack_dat quest/q650.dat
put_strings quest/q651.dat q651_87a1f20b_scp bin; repack_dat quest/q651.dat
put_strings quest/q652.dat q652_4e20ab43_scp bin; repack_dat quest/q652.dat
put_strings quest/q660.dat q660_f737718_scp bin; repack_dat quest/q660.dat
put_strings quest/q680.dat q680_51d704e4_scp bin; repack_dat quest/q680.dat
put_strings quest/q720.dat q720_bbe0d32e_scp bin; repack_dat quest/q720.dat
put_strings quest/q770.dat q770_59f68d25_scp bin; repack_dat quest/q770.dat
put_strings quest/q800.dat q800_bc7a2755_scp bin; repack_dat quest/q800.dat
put_strings quest/q801.dat q801_6c8f629a_scp bin; repack_dat quest/q801.dat
put_strings quest/q900.dat q900_626a2689_scp bin; repack_dat quest/q900.dat
put_strings quest/q910.dat q910_8d8ebfae_scp bin; repack_dat quest/q910.dat
put_strings quest/q920.dat q920_e5072c9_scp bin; repack_dat quest/q920.dat
put_strings quest/qab2.dat qab2_aec178b7_scp bin; repack_dat quest/qab2.dat
put_strings quest/qab3.dat qab3_934fd3b1_scp bin; repack_dat quest/qab3.dat
put_strings quest/qab5.dat qab5_4a1ea1bc_scp bin; repack_dat quest/qab5.dat
put_strings quest/qab6.dat qab6_69325679_scp bin; repack_dat quest/qab6.dat
put_strings quest/qaba.dat qaba_a7ed1850_scp bin; repack_dat quest/qaba.dat
put_strings quest/qabb.dat qabb_1e5a233e_scp bin; repack_dat quest/qabb.dat
put_strings quest/qabd.dat qabd_18ca8961_scp bin; repack_dat quest/qabd.dat
put_strings quest/qac8.dat qac8_fd8ac7ea_scp bin; repack_dat quest/qac8.dat
put_strings quest/qad0.dat qad0_c493efec_scp bin; repack_dat quest/qad0.dat
put_strings quest/qad1.dat qad1_55fcb9b3_scp bin; repack_dat quest/qad1.dat
put_strings quest/qad2.dat qad2_e6ef8eaf_scp bin; repack_dat quest/qad2.dat
put_strings quest/qad6.dat qad6_b6255483_scp bin; repack_dat quest/qad6.dat
put_strings quest/qaeb.dat qaeb_98b8e891_scp bin; repack_dat quest/qaeb.dat
put_strings quest/qaef.dat qaef_10112854_scp bin; repack_dat quest/qaef.dat
put_strings quest/qaf4.dat qaf4_e04e13b1_scp bin; repack_dat quest/qaf4.dat
put_strings quest/qb20.dat qb20_42c8efa_scp bin
put_strings quest/qb20.dat qb20_91cf1fa5_scp bin; repack_dat quest/qb20.dat
put_strings quest/qb40.dat qb40_f2a5ded9_scp bin
put_strings quest/qb40.dat qb40_b490bdc_scp bin
put_strings quest/qb40.dat qb40_ff6d92e9_scp bin
put_strings quest/qb40.dat qb40_9403a9bc_scp bin
put_strings quest/qb40.dat qb40_f7708d83_scp bin; repack_dat quest/qb40.dat
put_strings quest/qc10.dat qc10_ea55109b_scp bin; repack_dat quest/qc10.dat
put_strings quest/qc11.dat qc11_e05e7f97_scp bin; repack_dat quest/qc11.dat
put_strings quest/qc12.dat qc12_9b9e9b86_scp bin; repack_dat quest/qc12.dat
put_strings quest/qc30.dat qc30_fde14379_scp bin; repack_dat quest/qc30.dat
put_strings quest/qc50.dat qc50_de375136_scp bin; repack_dat quest/qc50.dat
put_strings st1/r100.dat r100_c723351a_scp bin; repack_dat st1/r100.dat
put_strings st1/r110.dat r110_be7ebe38_scp bin
put_strings st1/r110.dat r110_6b1cbecb_scp bin
put_strings st1/r110.dat r110_4ebc3b22_scp bin
put_strings st1/r110.dat r110_7fe2a715_scp bin
put_strings st1/r110.dat r110_7a562cb9_scp bin
put_strings st1/r110.dat r110_dd7422a2_scp bin; repack_dat st1/r110.dat
put_strings st1/r120.dat r120_f0d26b5d_scp bin; repack_dat st1/r120.dat
put_strings st1/r130.dat r130_e5cfdb23_scp bin
put_strings st1/r130.dat r130_12b5a85a_scp bin; repack_dat st1/r130.dat
put_strings st1/r140.dat r140_29cb90b_scp bin
put_strings st1/r140.dat r140_60377331_scp bin
put_strings st1/r140.dat r140_82d2caac_scp bin
put_strings st1/r140.dat r140_cd4fd96a_scp bin
put_strings st1/r140.dat r140_f82d8b66_scp bin
put_strings st1/r140.dat r140_657c1219_scp bin
put_strings st1/r140.dat r140_7e0bd84f_scp bin
put_strings st1/r140.dat r140_9fbdc6a2_scp bin
put_strings st1/r140.dat r140_dc76121c_scp bin
put_strings st1/r140.dat r140_ea0da2aa_scp bin
put_strings st1/r140.dat r140_336c5af9_scp bin
put_strings st1/r140.dat r140_49e73635_scp bin; repack_dat st1/r140.dat
put_strings st1/r150.dat r150_5ced6cf8_scp bin
put_strings st1/r150.dat r150_f100866e_scp bin
put_strings st1/r150.dat r150_df579346_scp bin; repack_dat st1/r150.dat
put_strings st1/r160.dat r160_3fa0647a_scp bin
put_strings st1/r160.dat r160_74d9b777_scp bin
put_strings st1/r160.dat r160_1557ce81_scp bin
put_strings st1/r160.dat r160_7247f0a7_scp bin
put_strings st1/r160.dat r160_307c8a44_scp bin
put_strings st1/r160.dat r160_f8f21cd2_scp bin
put_strings st1/r160.dat r160_19656865_scp bin
put_strings st1/r160.dat r160_e290faf0_scp bin
put_strings st1/r160.dat r160_dc20cee5_scp bin
put_strings st1/r160.dat r160_441c44e3_scp bin
put_strings st1/r160.dat r160_7cde1b3f_scp bin; repack_dat st1/r160.dat
put_strings st1/r170.dat r170_e7cef294_scp bin
put_strings st1/r170.dat r170_261956fa_scp bin; repack_dat st1/r170.dat
put_strings st2/r200.dat r200_427ea0a7_scp bin
put_strings st2/r200.dat r200_d52e3bf5_scp bin
put_strings st2/r200.dat r200_e684ee2d_scp bin
put_strings st2/r200.dat r200_c832af28_scp bin
put_strings st2/r200.dat r200_d4dad831_scp bin; repack_dat st2/r200.dat
put_strings st5/r530.dat r530_3c8107d_scp bin; repack_dat st5/r530.dat
put_strings subtitle/subtitle0010${LANG2}.dat subtitle0010 smd
put_strings subtitle/subtitle0011${LANG2}.dat subtitle0011 smd
put_strings subtitle/subtitle0030${LANG2}.dat subtitle0030 smd
put_strings subtitle/subtitle0031${LANG2}.dat subtitle0031 smd
put_strings subtitle/subtitle0040${LANG2}.dat subtitle0040 smd
put_strings subtitle/subtitle0050${LANG2}.dat subtitle0050 smd
put_strings subtitle/subtitle0055${LANG2}.dat subtitle0055 smd
put_strings subtitle/subtitle0060${LANG2}.dat subtitle0060 smd
put_strings subtitle/subtitle0080${LANG2}.dat subtitle0080 smd
put_strings subtitle/subtitle0081${LANG2}.dat subtitle0081 smd
put_strings subtitle/subtitle0086${LANG2}.dat subtitle0086 smd
put_strings subtitle/subtitle0090${LANG2}.dat subtitle0090 smd
put_strings subtitle/subtitle0091${LANG2}.dat subtitle0091 smd
put_strings subtitle/subtitle0092${LANG2}.dat subtitle0092 smd
put_strings subtitle/subtitle0110${LANG2}.dat subtitle0110 smd
put_strings subtitle/subtitle0111${LANG2}.dat subtitle0111 smd
put_strings subtitle/subtitle0120${LANG2}.dat subtitle0120 smd
put_strings subtitle/subtitle0130${LANG2}.dat subtitle0130 smd
put_strings subtitle/subtitle0140${LANG2}.dat subtitle0140 smd
put_strings subtitle/subtitle0160${LANG2}.dat subtitle0160 smd
put_strings subtitle/subtitle0170${LANG2}.dat subtitle0170 smd
put_strings subtitle/subtitle0190${LANG2}.dat subtitle0190 smd
put_strings subtitle/subtitle0191${LANG2}.dat subtitle0191 smd
put_strings subtitle/subtitle0225${LANG2}.dat subtitle0225 smd
put_strings subtitle/subtitle0226${LANG2}.dat subtitle0226 smd
put_strings subtitle/subtitle0230${LANG2}.dat subtitle0230 smd
put_strings subtitle/subtitle0240${LANG2}.dat subtitle0240 smd
put_strings subtitle/subtitle0241${LANG2}.dat subtitle0241 smd
put_strings subtitle/subtitle0250${LANG2}.dat subtitle0250 smd
put_strings subtitle/subtitle0251${LANG2}.dat subtitle0251 smd
put_strings subtitle/subtitle0260${LANG2}.dat subtitle0260 smd
put_strings subtitle/subtitle0262${LANG2}.dat subtitle0262 smd
put_strings subtitle/subtitle0270${LANG2}.dat subtitle0270 smd
put_strings subtitle/subtitle0280${LANG2}.dat subtitle0280 smd
put_strings subtitle/subtitle0300${LANG2}.dat subtitle0300 smd
put_strings subtitle/subtitle0301${LANG2}.dat subtitle0301 smd
put_strings subtitle/subtitle0310${LANG2}.dat subtitle0310 smd
put_strings subtitle/subtitle0311${LANG2}.dat subtitle0311 smd
put_strings subtitle/subtitle0320${LANG2}.dat subtitle0320 smd
put_strings subtitle/subtitle0321${LANG2}.dat subtitle0321 smd
put_strings subtitle/subtitle0322${LANG2}.dat subtitle0322 smd
put_strings subtitle/subtitle0323${LANG2}.dat subtitle0323 smd
put_strings subtitle/subtitle0325${LANG2}.dat subtitle0325 smd
put_strings subtitle/subtitle0326${LANG2}.dat subtitle0326 smd
put_strings subtitle/subtitle0330${LANG2}.dat subtitle0330 smd
put_strings subtitle/subtitle0340${LANG2}.dat subtitle0340 smd
put_strings subtitle/subtitle0341${LANG2}.dat subtitle0341 smd
put_strings subtitle/subtitle0350${LANG2}.dat subtitle0350 smd
put_strings subtitle/subtitle0351${LANG2}.dat subtitle0351 smd
put_strings subtitle/subtitle0352${LANG2}.dat subtitle0352 smd
put_strings subtitle/subtitle0360${LANG2}.dat subtitle0360 smd
put_strings subtitle/subtitle0370${LANG2}.dat subtitle0370 smd
put_strings subtitle/subtitle0390${LANG2}.dat subtitle0390 smd
put_strings subtitle/subtitle0400${LANG2}.dat subtitle0400 smd
put_strings subtitle/subtitle0410${LANG2}.dat subtitle0410 smd
put_strings subtitle/subtitle0420${LANG2}.dat subtitle0420 smd
put_strings subtitle/subtitle0440${LANG2}.dat subtitle0440 smd
put_strings subtitle/subtitle0441${LANG2}.dat subtitle0441 smd
put_strings subtitle/subtitle0460${LANG2}.dat subtitle0460 smd
put_strings subtitle/subtitle0461${LANG2}.dat subtitle0461 smd
put_strings subtitle/subtitle0470${LANG2}.dat subtitle0470 smd
put_strings subtitle/subtitle0471${LANG2}.dat subtitle0471 smd
put_strings subtitle/subtitle0475${LANG2}.dat subtitle0475 smd
put_strings subtitle/subtitle0480${LANG2}.dat subtitle0480 smd
put_strings subtitle/subtitle0482${LANG2}.dat subtitle0482 smd
put_strings subtitle/subtitle0483${LANG2}.dat subtitle0483 smd
put_strings subtitle/subtitle0485${LANG2}.dat subtitle0485 smd
put_strings subtitle/subtitle0490${LANG2}.dat subtitle0490 smd
put_strings subtitle/subtitle0491${LANG2}.dat subtitle0491 smd
put_strings subtitle/subtitle0500${LANG2}.dat subtitle0500 smd
put_strings subtitle/subtitle0502${LANG2}.dat subtitle0502 smd
put_strings subtitle/subtitle0520${LANG2}.dat subtitle0520 smd
put_strings subtitle/subtitle0521${LANG2}.dat subtitle0521 smd
put_strings subtitle/subtitle0525${LANG2}.dat subtitle0525 smd
put_strings subtitle/subtitle0526${LANG2}.dat subtitle0526 smd
put_strings subtitle/subtitle0530${LANG2}.dat subtitle0530 smd
put_strings subtitle/subtitle0531${LANG2}.dat subtitle0531 smd
put_strings subtitle/subtitle0540${LANG2}.dat subtitle0540 smd
put_strings subtitle/subtitle0550${LANG2}.dat subtitle0550 smd
put_strings subtitle/subtitle0552${LANG2}.dat subtitle0552 smd
put_strings subtitle/subtitle0570${LANG2}.dat subtitle0570 smd
put_strings subtitle/subtitle0571${LANG2}.dat subtitle0571 smd
put_strings subtitle/subtitle0590${LANG2}.dat subtitle0590 smd
put_strings subtitle/subtitle0600${LANG2}.dat subtitle0600 smd
put_strings subtitle/subtitle0610${LANG2}.dat subtitle0610 smd
put_strings subtitle/subtitle0612${LANG2}.dat subtitle0612 smd
put_strings subtitle/subtitle0630${LANG2}.dat subtitle0630 smd
put_strings subtitle/subtitle0631${LANG2}.dat subtitle0631 smd
put_strings subtitle/subtitle0640${LANG2}.dat subtitle0640 smd
put_strings subtitle/subtitle0642${LANG2}.dat subtitle0642 smd
put_strings subtitle/subtitle0650${LANG2}.dat subtitle0650 smd
put_strings subtitle/subtitle0651${LANG2}.dat subtitle0651 smd
put_strings subtitle/subtitle0655${LANG2}.dat subtitle0655 smd
put_strings subtitle/subtitle0656${LANG2}.dat subtitle0656 smd
put_strings subtitle/subtitle0660${LANG2}.dat subtitle0660 smd
put_strings subtitle/subtitle0661${LANG2}.dat subtitle0661 smd
put_strings subtitle/subtitle0670${LANG2}.dat subtitle0670 smd
put_strings subtitle/subtitle0671${LANG2}.dat subtitle0671 smd
put_strings subtitle/subtitle0680${LANG2}.dat subtitle0680 smd
put_strings subtitle/subtitle0682${LANG2}.dat subtitle0682 smd
put_strings subtitle/subtitle0690${LANG2}.dat subtitle0690 smd
put_strings subtitle/subtitle0692${LANG2}.dat subtitle0692 smd
put_strings subtitle/subtitle0693${LANG2}.dat subtitle0693 smd
put_strings subtitle/subtitle0694${LANG2}.dat subtitle0694 smd
put_strings subtitle/subtitle0700${LANG2}.dat subtitle0700 smd
put_strings subtitle/subtitle0702${LANG2}.dat subtitle0702 smd
put_strings subtitle/subtitle0720${LANG2}.dat subtitle0720 smd
put_strings subtitle/subtitle0722${LANG2}.dat subtitle0722 smd
put_strings subtitle/subtitle0730${LANG2}.dat subtitle0730 smd
put_strings subtitle/subtitle0760${LANG2}.dat subtitle0760 smd
put_strings subtitle/subtitle0761${LANG2}.dat subtitle0761 smd
put_strings subtitle/subtitle0770${LANG2}.dat subtitle0770 smd
put_strings subtitle/subtitle0771${LANG2}.dat subtitle0771 smd
put_strings subtitle/subtitle0780${LANG2}.dat subtitle0780 smd
put_strings subtitle/subtitle0781${LANG2}.dat subtitle0781 smd
put_strings subtitle/subtitle0790${LANG2}.dat subtitle0790 smd
put_strings subtitle/subtitle0791${LANG2}.dat subtitle0791 smd
put_strings subtitle/subtitle0792${LANG2}.dat subtitle0792 smd
put_strings subtitle/subtitle0800${LANG2}.dat subtitle0800 smd
put_strings subtitle/subtitle0810${LANG2}.dat subtitle0810 smd
put_strings subtitle/subtitle0811${LANG2}.dat subtitle0811 smd
put_strings subtitle/subtitle0820${LANG2}.dat subtitle0820 smd
put_strings subtitle/subtitle0830${LANG2}.dat subtitle0830 smd
put_strings subtitle/subtitle0835${LANG2}.dat subtitle0835 smd
put_strings subtitle/subtitle0836${LANG2}.dat subtitle0836 smd
put_strings subtitle/subtitle0850${LANG2}.dat subtitle0850 smd
put_strings subtitle/subtitle0855${LANG2}.dat subtitle0855 smd
put_strings subtitle/subtitle0860${LANG2}.dat subtitle0860 smd
put_strings subtitle/subtitle0861${LANG2}.dat subtitle0861 smd
put_strings subtitle/subtitle0870${LANG2}.dat subtitle0870 smd
put_strings subtitle/subtitle0871${LANG2}.dat subtitle0871 smd
put_strings subtitle/subtitle0875${LANG2}.dat subtitle0875 smd
put_strings subtitle/subtitle0880${LANG2}.dat subtitle0880 smd
put_strings subtitle/subtitle0900${LANG2}.dat subtitle0900 smd
put_strings subtitle/subtitle0901${LANG2}.dat subtitle0901 smd
put_strings subtitle/subtitle0910${LANG2}.dat subtitle0910 smd
put_strings subtitle/subtitle0920${LANG2}.dat subtitle0920 smd
put_strings subtitle/subtitle0921${LANG2}.dat subtitle0921 smd
put_strings subtitle/subtitle0926${LANG2}.dat subtitle0926 smd
put_strings subtitle/subtitle0930${LANG2}.dat subtitle0930 smd
put_strings subtitle/subtitle0931${LANG2}.dat subtitle0931 smd
put_strings subtitle/subtitle0935${LANG2}.dat subtitle0935 smd
put_strings subtitle/subtitle0936${LANG2}.dat subtitle0936 smd
put_strings subtitle/subtitle0940${LANG2}.dat subtitle0940 smd
put_strings subtitle/subtitle0950${LANG2}.dat subtitle0950 smd
put_strings subtitle/subtitle0951${LANG2}.dat subtitle0951 smd
put_strings subtitle/subtitle0960${LANG2}.dat subtitle0960 smd
put_strings subtitle/subtitle0961${LANG2}.dat subtitle0961 smd
put_strings subtitle/subtitle0970${LANG2}.dat subtitle0970 smd
put_strings subtitle/subtitle0990${LANG2}.dat subtitle0990 smd
put_strings subtitle/subtitle1000${LANG2}.dat subtitle1000 smd
put_strings subtitle/subtitle1001${LANG2}.dat subtitle1001 smd
put_strings subtitle/subtitle1010${LANG2}.dat subtitle1010 smd
put_strings subtitle/subtitle1030${LANG2}.dat subtitle1030 smd
put_strings subtitle/subtitle1040${LANG2}.dat subtitle1040 smd
put_strings subtitle/subtitle1041${LANG2}.dat subtitle1041 smd
put_strings subtitle/subtitle1050${LANG2}.dat subtitle1050 smd
put_strings subtitle/subtitle1051${LANG2}.dat subtitle1051 smd
put_strings subtitle/subtitle1060${LANG2}.dat subtitle1060 smd
put_strings subtitle/subtitle1080${LANG2}.dat subtitle1080 smd
put_strings subtitle/subtitle1090${LANG2}.dat subtitle1090 smd
put_strings subtitle/subtitle1091${LANG2}.dat subtitle1091 smd
put_strings subtitle/subtitle1100${LANG2}.dat subtitle1100 smd
put_strings subtitle/subtitle1120${LANG2}.dat subtitle1120 smd
put_strings subtitle/subtitle1121${LANG2}.dat subtitle1121 smd
put_strings subtitle/subtitle1125${LANG2}.dat subtitle1125 smd
put_strings subtitle/subtitle1150${LANG2}.dat subtitle1150 smd
put_strings subtitle/subtitle1160${LANG2}.dat subtitle1160 smd
put_strings subtitle/subtitle1180${LANG2}.dat subtitle1180 smd
put_strings subtitle/subtitle1181${LANG2}.dat subtitle1181 smd
put_strings subtitle/subtitle1190${LANG2}.dat subtitle1190 smd
put_strings subtitle/subtitle1191${LANG2}.dat subtitle1191 smd
put_strings subtitle/subtitle1210${LANG2}.dat subtitle1210 smd
put_strings subtitle/subtitle1211${LANG2}.dat subtitle1211 smd
put_strings subtitle/subtitle1220${LANG2}.dat subtitle1220 smd
put_strings subtitle/subtitle1221${LANG2}.dat subtitle1221 smd
put_strings subtitle/subtitle1230${LANG2}.dat subtitle1230 smd
put_strings subtitle/subtitle1232${LANG2}.dat subtitle1232 smd
put_strings subtitle/subtitle1233${LANG2}.dat subtitle1233 smd
put_strings subtitle/subtitle1234${LANG2}.dat subtitle1234 smd
put_strings subtitle/subtitle1235${LANG2}.dat subtitle1235 smd
put_strings subtitle/subtitle1240${LANG2}.dat subtitle1240 smd
put_strings subtitle/subtitle1241${LANG2}.dat subtitle1241 smd
put_strings subtitle/subtitle1250${LANG2}.dat subtitle1250 smd
put_strings subtitle/subtitle1260${LANG2}.dat subtitle1260 smd
put_strings subtitle/subtitle1270${LANG2}.dat subtitle1270 smd
put_strings subtitle/subtitle1280${LANG2}.dat subtitle1280 smd
put_strings subtitle/subtitle1290${LANG2}.dat subtitle1290 smd
put_strings subtitle/subtitle1300${LANG2}.dat subtitle1300 smd
put_strings subtitle/subtitle1310${LANG2}.dat subtitle1310 smd
put_strings subtitle/subtitle1320${LANG2}.dat subtitle1320 smd
put_strings subtitle/subtitle1400${LANG2}.dat subtitle1400 smd
put_strings subtitle/subtitle1402${LANG2}.dat subtitle1402 smd
put_strings subtitle/subtitleb060${LANG2}.dat subtitleb060 smd
put_strings subtitle/subtitleb191${LANG2}.dat subtitleb191 smd
put_strings subtitle/subtitleb251${LANG2}.dat subtitleb251 smd
put_strings subtitle/subtitleb301${LANG2}.dat subtitleb301 smd
put_strings subtitle/subtitleb311${LANG2}.dat subtitleb311 smd
put_strings subtitle/subtitleb321${LANG2}.dat subtitleb321 smd
put_strings subtitle/subtitleb341${LANG2}.dat subtitleb341 smd
put_strings subtitle/subtitleb351${LANG2}.dat subtitleb351 smd
put_strings subtitle/subtitleb441${LANG2}.dat subtitleb441 smd
put_strings subtitle/subtitleb461${LANG2}.dat subtitleb461 smd
put_strings subtitle/subtitleb471${LANG2}.dat subtitleb471 smd
put_strings subtitle/subtitleb651${LANG2}.dat subtitleb651 smd
put_strings subtitle/subtitleb656${LANG2}.dat subtitleb656 smd
put_strings subtitle/subtitleb661${LANG2}.dat subtitleb661 smd
put_strings subtitle/subtitleb671${LANG2}.dat subtitleb671 smd
put_strings txtmess/txt_chapter${LANG2}.dat txt_chapter tmd
put_strings txtmess/txt_core_add${LANG2}.dat txt_core_add tmd
put_strings txtmess/txt_core${LANG2}.dat txt_core tmd
put_strings txtmess/txt_credit${LANG2}.dat txt_credit tmd
put_strings txtmess/txt_dlc1${LANG2}.dat txt_dlc1 tmd
put_strings txtmess/txt_dlc2${LANG2}.dat txt_dlc2 tmd
put_strings txtmess/txt_dlc3${LANG2}.dat txt_dlc3 tmd
put_strings txtmess/txt_hud_add${LANG2}.dat txt_hud_add tmd
put_strings txtmess/txt_hud${LANG2}.dat txt_hud tmd
put_strings txtmess/txt_pause_add${LANG2}.dat txt_pause_add tmd
put_strings txtmess/txt_pause${LANG2}.dat txt_pause tmd
put_strings txtmess/txt_shop${LANG2}.dat txt_shop tmd
put_strings txtmess/txt_support${LANG2}.dat txt_support tmd
put_strings ui/ui_chapter${LANG2}.dat messchapter mcd
put_strings ui/ui_core_2${LANG2}.dat messcore_2 mcd
put_strings ui/ui_core_pc${LANG2}.dat messcore_pc mcd
put_strings ui/ui_core${LANG2}.dat messcore mcd
put_strings ui/ui_credit${LANG2}.dat messcredit mcd
put_strings ui/ui_dbg${LANG2}.dat messdbg mcd
put_strings ui/ui_dlc1${LANG2}.dat messdlc1 mcd
put_strings ui/ui_dlc2${LANG2}.dat messdlc2 mcd
put_strings ui/ui_dlc3${LANG2}.dat messdlc3 mcd
put_strings ui/ui_ending_dlc${LANG2}.dat messending_dlc mcd
put_strings ui/ui_ending${LANG2}.dat messending mcd
put_strings ui/ui_event${LANG2}.dat messevent mcd
put_strings ui/ui_hud_hacking${LANG2}.dat messhud_hacking mcd
put_strings ui/ui_hud${LANG2}.dat messhud mcd
put_strings ui/ui_loading.dat messloading mcd
put_strings ui/ui_option${LANG2}.dat messoption mcd
put_strings ui/ui_pause${LANG2}.dat messpause mcd
put_strings ui/ui_shop${LANG2}.dat messshop mcd
put_strings ui/ui_title${LANG2}.dat messtitle mcd
put_strings wd1/g11516.dat g11516_2ccba2ea_scp bin; repack_dat wd1/g11516.dat
put_strings novel M1030_S0310_N${LANG3} txt
put_strings novel M1070_S0020_N${LANG3} txt
put_strings novel M1070_S0040_N${LANG3} txt
put_strings novel M1070_S0060_N${LANG3} txt
put_strings novel M1070_S0080_N${LANG3} txt
put_strings novel M1070_S0100_N${LANG3} txt
put_strings novel M3060_S0005_N${LANG3} txt
put_strings novel M3060_S0035_GM_N${LANG3} txt
put_strings novel M3060_S0910_N${LANG3} txt
put_strings novel M6010_S0050_N${LANG3} txt
put_strings novel M6010_S0150_N${LANG3} txt
put_strings novel M6010_S0250_N${LANG3} txt
put_strings novel M9000_S0500_N${LANG3} txt
put_strings novel M5095_S0020_N${LANG3} txt
put_strings novel M5095_S0025_N${LANG3} txt
put_strings novel M5095_S0100_N${LANG3} txt
put_strings novel M5095_S0200_N${LANG3} txt
put_strings novel M5095_S0300_N${LANG3} txt
