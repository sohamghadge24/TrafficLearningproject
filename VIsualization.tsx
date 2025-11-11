import React, { useState, useMemo } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ErrorBar, ScatterChart, Scatter } from 'recharts';
import { TrendingUp, TrendingDown, Activity, BarChart3 } from 'lucide-react';

const TrafficMetricsVisualization = () => {
  const [selectedView, setSelectedView] = useState('overview');
  const [selectedScenario, setSelectedScenario] = useState('all');

  // Parse the metrics data
  const metricsData = {
    "episodes": [
        {"episode": 1, "scenario": "medium", "reward": 3609.371581907384, "avg_cost": 0.048709326684474946, "steps": 3600},
        {"episode": 2, "scenario": "high", "reward": 3566.77270154655, "avg_cost": 0.04971971999970265, "steps": 3600},
        {"episode": 3, "scenario": "low", "reward": 3566.189090117812, "avg_cost": 0.050014850600208674, "steps": 3600},
        {"episode": 4, "scenario": "medium", "reward": 3584.07757537812, "avg_cost": 0.04878446652864416, "steps": 3600},
        {"episode": 5, "scenario": "high", "reward": 3559.059115776792, "avg_cost": 0.05022827495393964, "steps": 3600},
        {"episode": 6, "scenario": "low", "reward": 3554.6364091821015, "avg_cost": 0.05081112952928783, "steps": 3600},
        {"episode": 7, "scenario": "medium", "reward": 3627.398582600057, "avg_cost": 0.04535286745043575, "steps": 3600},
        {"episode": 8, "scenario": "high", "reward": 3573.790864687413, "avg_cost": 0.0478800078559046, "steps": 3600},
        {"episode": 9, "scenario": "low", "reward": 3587.248308603652, "avg_cost": 0.04678387852243355, "steps": 3600},
        {"episode": 10, "scenario": "medium", "reward": 3679.0816866979003, "avg_cost": 0.04085376914189611, "steps": 3600},
        {"episode": 11, "scenario": "high", "reward": 3612.5190879396687, "avg_cost": 0.04577486629002831, "steps": 3600},
        {"episode": 12, "scenario": "low", "reward": 3662.0476196333766, "avg_cost": 0.04176358496834938, "steps": 3600},
        {"episode": 13, "scenario": "medium", "reward": 3610.4820339009166, "avg_cost": 0.04498624093895261, "steps": 3600},
        {"episode": 14, "scenario": "high", "reward": 3613.4614428915083, "avg_cost": 0.045842427564655536, "steps": 3600},
        {"episode": 15, "scenario": "low", "reward": 3616.0646539852023, "avg_cost": 0.045484579626936465, "steps": 3600},
        {"episode": 16, "scenario": "medium", "reward": 3620.3806187584996, "avg_cost": 0.04291566354998698, "steps": 3600},
        {"episode": 17, "scenario": "high", "reward": 3663.394626740366, "avg_cost": 0.04222198530475402, "steps": 3600},
        {"episode": 18, "scenario": "low", "reward": 3676.0856663547456, "avg_cost": 0.03907644251309749, "steps": 3600},
        {"episode": 19, "scenario": "medium", "reward": 3643.1362985372543, "avg_cost": 0.04030188520102658, "steps": 3600},
        {"episode": 20, "scenario": "high", "reward": 3642.567687615752, "avg_cost": 0.04521966206718288, "steps": 3600},
        {"episode": 21, "scenario": "low", "reward": 3690.7961995899677, "avg_cost": 0.041505660952405175, "steps": 3600},
        {"episode": 22, "scenario": "medium", "reward": 3651.595031723613, "avg_cost": 0.04122861586006669, "steps": 3600},
        {"episode": 23, "scenario": "high", "reward": 3643.616861135699, "avg_cost": 0.04018535864875755, "steps": 3600},
        {"episode": 24, "scenario": "low", "reward": 3681.935973027721, "avg_cost": 0.039157497718568066, "steps": 3600},
        {"episode": 25, "scenario": "medium", "reward": 3653.5980524867773, "avg_cost": 0.04111522761936713, "steps": 3600},
        {"episode": 26, "scenario": "high", "reward": 3719.8901575282216, "avg_cost": 0.036056319330301546, "steps": 3600},
        {"episode": 27, "scenario": "low", "reward": 3661.029302030802, "avg_cost": 0.03744646358743517, "steps": 3600},
        {"episode": 28, "scenario": "medium", "reward": 3690.5480067692697, "avg_cost": 0.038756578492983765, "steps": 3600},
        {"episode": 29, "scenario": "high", "reward": 3713.414301607758, "avg_cost": 0.03525992345459397, "steps": 3600},
        {"episode": 30, "scenario": "low", "reward": 3678.931859964505, "avg_cost": 0.04017651325421563, "steps": 3600},
        {"episode": 31, "scenario": "medium", "reward": 3677.767112794332, "avg_cost": 0.039569405650383686, "steps": 3600},
        {"episode": 32, "scenario": "high", "reward": 3692.2310695564374, "avg_cost": 0.040142858549047054, "steps": 3600},
        {"episode": 33, "scenario": "low", "reward": 3643.9994033025578, "avg_cost": 0.04187616913333639, "steps": 3600},
        {"episode": 34, "scenario": "medium", "reward": 3620.4819653220475, "avg_cost": 0.04419228557549003, "steps": 3600},
        {"episode": 35, "scenario": "high", "reward": 3647.0112550519407, "avg_cost": 0.041475738388512075, "steps": 3600},
        {"episode": 36, "scenario": "low", "reward": 3640.6222930923104, "avg_cost": 0.04171071352863995, "steps": 3600},
        {"episode": 37, "scenario": "medium", "reward": 3694.7456052042544, "avg_cost": 0.03725184047478251, "steps": 3600},
        {"episode": 38, "scenario": "high", "reward": 3702.824041072279, "avg_cost": 0.03561324296079369, "steps": 3600},
        {"episode": 39, "scenario": "low", "reward": 3702.104843109846, "avg_cost": 0.03671400816580798, "steps": 3600},
        {"episode": 40, "scenario": "medium", "reward": 3724.1816111430526, "avg_cost": 0.03518541109625302, "steps": 3600},
        {"episode": 41, "scenario": "high", "reward": 3688.836718515493, "avg_cost": 0.04027759779490427, "steps": 3600},
        {"episode": 42, "scenario": "low", "reward": 3667.224218430347, "avg_cost": 0.038173660438430186, "steps": 3600},
        {"episode": 43, "scenario": "medium", "reward": 3661.305141042918, "avg_cost": 0.041032066849163835, "steps": 3600},
        {"episode": 44, "scenario": "high", "reward": 3686.7743682339787, "avg_cost": 0.03642390702993402, "steps": 3600},
        {"episode": 45, "scenario": "low", "reward": 3677.1184025481343, "avg_cost": 0.03958869523815035, "steps": 3600},
        {"episode": 46, "scenario": "medium", "reward": 3681.8432388082147, "avg_cost": 0.041355037712556726, "steps": 3600},
        {"episode": 47, "scenario": "high", "reward": 3724.2799911648035, "avg_cost": 0.03603558252856601, "steps": 3600},
        {"episode": 48, "scenario": "low", "reward": 3693.9614757616073, "avg_cost": 0.03776322969080259, "steps": 3600},
        {"episode": 49, "scenario": "medium", "reward": 3707.6408310085535, "avg_cost": 0.03496910267858766, "steps": 3600},
        {"episode": 50, "scenario": "high", "reward": 3724.4688118696213, "avg_cost": 0.035553424751851706, "steps": 3600},
        {"episode": 51, "scenario": "low", "reward": 3682.043569236994, "avg_cost": 0.039258564620524544, "steps": 3600},
        {"episode": 52, "scenario": "medium", "reward": 3682.7258795797825, "avg_cost": 0.038189303238048325, "steps": 3600},
        {"episode": 53, "scenario": "high", "reward": 3675.6590832024813, "avg_cost": 0.03808112420956604, "steps": 3600},
        {"episode": 54, "scenario": "low", "reward": 3671.2177243139595, "avg_cost": 0.039040495521104376, "steps": 3600},
        {"episode": 55, "scenario": "medium", "reward": 3665.97301415354, "avg_cost": 0.039740701029465225, "steps": 3600},
        {"episode": 56, "scenario": "high", "reward": 3582.6943525373936, "avg_cost": 0.04750837772476694, "steps": 3600},
        {"episode": 57, "scenario": "low", "reward": 3669.4677257947624, "avg_cost": 0.04246310715589465, "steps": 3600},
        {"episode": 58, "scenario": "medium", "reward": 3648.4033484384418, "avg_cost": 0.04233284636892171, "steps": 3600},
        {"episode": 59, "scenario": "high", "reward": 3618.546122074127, "avg_cost": 0.044635441603346, "steps": 3600},
        {"episode": 60, "scenario": "low", "reward": 3632.8602818511426, "avg_cost": 0.0432413603449499, "steps": 3600},
        {"episode": 61, "scenario": "medium", "reward": 3668.945661276579, "avg_cost": 0.04308121739201144, "steps": 3600},
        {"episode": 62, "scenario": "high", "reward": 3646.4128178432584, "avg_cost": 0.043126168486713946, "steps": 3600},
        {"episode": 63, "scenario": "low", "reward": 3640.547647830099, "avg_cost": 0.04527839795414669, "steps": 3600},
        {"episode": 64, "scenario": "medium", "reward": 3622.775025218725, "avg_cost": 0.04558547599667994, "steps": 3600},
        {"episode": 65, "scenario": "high", "reward": 3624.782853424549, "avg_cost": 0.04431068003449279, "steps": 3600},
        {"episode": 66, "scenario": "low", "reward": 3639.1274519711733, "avg_cost": 0.044248141488060354, "steps": 3600},
        {"episode": 67, "scenario": "medium", "reward": 3635.8406223505735, "avg_cost": 0.042930198347247726, "steps": 3600},
        {"episode": 68, "scenario": "high", "reward": 3640.4297035709023, "avg_cost": 0.04468735639174055, "steps": 3600},
        {"episode": 69, "scenario": "low", "reward": 3606.071493335068, "avg_cost": 0.04466948418632253, "steps": 3600},
        {"episode": 70, "scenario": "medium", "reward": 3587.2380652800202, "avg_cost": 0.04607337621234668, "steps": 3600},
        {"episode": 71, "scenario": "high", "reward": 3670.0109682972543, "avg_cost": 0.04337088435409694, "steps": 3600},
        {"episode": 72, "scenario": "low", "reward": 3608.069712864235, "avg_cost": 0.04353524229799708, "steps": 3600},
        {"episode": 73, "scenario": "medium", "reward": 3597.3105133399367, "avg_cost": 0.04346315145363203, "steps": 3600},
        {"episode": 74, "scenario": "high", "reward": 3648.9471947122365, "avg_cost": 0.04171889217660969, "steps": 3600},
        {"episode": 75, "scenario": "low", "reward": 3653.880804270506, "avg_cost": 0.041904638342093674, "steps": 3600},
        {"episode": 76, "scenario": "medium", "reward": 3627.422016493976, "avg_cost": 0.043616482328054394, "steps": 3600},
        {"episode": 77, "scenario": "high", "reward": 3604.3164793252945, "avg_cost": 0.04648201218883818, "steps": 3600},
        {"episode": 78, "scenario": "low", "reward": 3617.375105470419, "avg_cost": 0.0450437707050393, "steps": 3600},
        {"episode": 79, "scenario": "medium", "reward": 3639.514451660216, "avg_cost": 0.04357177461937277, "steps": 3600},
        {"episode": 80, "scenario": "high", "reward": 3602.794404366985, "avg_cost": 0.04724283674938811, "steps": 3600},
        {"episode": 81, "scenario": "low", "reward": 3627.22025263682, "avg_cost": 0.04321964448033314, "steps": 3600},
        {"episode": 82, "scenario": "medium", "reward": 3625.7980970442295, "avg_cost": 0.0461597760359291, "steps": 3600},
        {"episode": 83, "scenario": "high", "reward": 3632.184499949217, "avg_cost": 0.04517253001117044, "steps": 3600},
        {"episode": 84, "scenario": "low", "reward": 3631.849442921579, "avg_cost": 0.046211433270493416, "steps": 3600},
        {"episode": 85, "scenario": "medium", "reward": 3628.860014837235, "avg_cost": 0.04261671469236414, "steps": 3600},
        {"episode": 86, "scenario": "high", "reward": 3646.7873845025897, "avg_cost": 0.044398802859812146, "steps": 3600},
        {"episode": 87, "scenario": "low", "reward": 3615.6980182379484, "avg_cost": 0.042300388641370874, "steps": 3600},
        {"episode": 88, "scenario": "medium", "reward": 3609.4824992120266, "avg_cost": 0.044982020043405804, "steps": 3600},
        {"episode": 89, "scenario": "high", "reward": 3658.953507885337, "avg_cost": 0.03895979326063146, "steps": 3600},
        {"episode": 90, "scenario": "low", "reward": 3622.5761871412396, "avg_cost": 0.043700359528754944, "steps": 3600},
        {"episode": 91, "scenario": "medium", "reward": 3669.8516094954684, "avg_cost": 0.03926404591921406, "steps": 3600},
        {"episode": 92, "scenario": "high", "reward": 3636.121677365154, "avg_cost": 0.041688521436816596, "steps": 3600},
        {"episode": 93, "scenario": "low", "reward": 3687.1660088519566, "avg_cost": 0.039455190730902055, "steps": 3600},
        {"episode": 94, "scenario": "medium", "reward": 3692.7639315724373, "avg_cost": 0.03960139117268328, "steps": 3600},
        {"episode": 95, "scenario": "high", "reward": 3679.7297695167363, "avg_cost": 0.03951586709862265, "steps": 3600},
        {"episode": 96, "scenario": "low", "reward": 3708.1087877452374, "avg_cost": 0.0378616804716229, "steps": 3600},
        {"episode": 97, "scenario": "medium", "reward": 3634.908558386378, "avg_cost": 0.04258831636145866, "steps": 3600},
        {"episode": 98, "scenario": "high", "reward": 3648.5735728368163, "avg_cost": 0.043209506611068114, "steps": 3600},
        {"episode": 99, "scenario": "low", "reward": 3661.2709037438035, "avg_cost": 0.03912683849598074, "steps": 3600},
        {"episode": 100, "scenario": "medium", "reward": 3656.030786031857, "avg_cost": 0.04314757017030691, "steps": 3600},
        {"episode": 101, "scenario": "high", "reward": 3679.4401100613177, "avg_cost": 0.03863772080946041, "steps": 3600},
        {"episode": 102, "scenario": "low", "reward": 3649.591852091253, "avg_cost": 0.042036787608651344, "steps": 3600},
        {"episode": 103, "scenario": "medium", "reward": 3654.0312346220016, "avg_cost": 0.04227126345885659, "steps": 3600},
        {"episode": 104, "scenario": "high", "reward": 3717.2522261440754, "avg_cost": 0.03691559412199745, "steps": 3600},
        {"episode": 105, "scenario": "low", "reward": 3633.5705131217837, "avg_cost": 0.04391193619567073, "steps": 3600},
        {"episode": 106, "scenario": "medium", "reward": 3647.331252552569, "avg_cost": 0.041260122444299566, "steps": 3600},
        {"episode": 107, "scenario": "high", "reward": 3673.650302954018, "avg_cost": 0.04131774807827444, "steps": 3600},
        {"episode": 108, "scenario": "low", "reward": 3663.4731290750206, "avg_cost": 0.04102672267226606, "steps": 3600},
        {"episode": 109, "scenario": "medium", "reward": 3686.9578673020005, "avg_cost": 0.03970499330989292, "steps": 3600},
        {"episode": 110, "scenario": "high", "reward": 3640.2556263506413, "avg_cost": 0.04261255219242432, "steps": 3600},
        {"episode": 111, "scenario": "low", "reward": 3673.6345950104296, "avg_cost": 0.04005389427442828, "steps": 3600},
        {"episode": 112, "scenario": "medium", "reward": 3693.4581343960017, "avg_cost": 0.03883258583696766, "steps": 3600},
        {"episode": 113, "scenario": "high", "reward": 3640.129905823618, "avg_cost": 0.04061454974528816, "steps": 3600},
        {"episode": 114, "scenario": "low", "reward": 3679.8282866366208, "avg_cost": 0.03695597650657874, "steps": 3600},
        {"episode": 115, "scenario": "medium", "reward": 3687.6775586493313, "avg_cost": 0.038899899239056845, "steps": 3600},
        {"episode": 116, "scenario": "high", "reward": 3725.2633107490838, "avg_cost": 0.038011055916884084, "steps": 3600},
        {"episode": 117, "scenario": "low", "reward": 3691.9016374982893, "avg_cost": 0.039325473157870064, "steps": 3600},
        {"episode": 118, "scenario": "medium", "reward": 3679.6532541811466, "avg_cost": 0.039459947829600425, "steps": 3600},
        {"episode": 119, "scenario": "high", "reward": 3669.574526593089, "avg_cost": 0.04039625603472814, "steps": 3600},
        {"episode": 120, "scenario": "low", "reward": 3700.58265042305, "avg_cost": 0.03899951351703041, "steps": 3600},
        {"episode": 121, "scenario": "medium", "reward": 3685.158345848322, "avg_cost": 0.03758985608525109, "steps": 3600},
        {"episode": 122, "scenario": "high", "reward": 3663.7373986914754, "avg_cost": 0.04006386735774059, "steps": 3600},
        {"episode": 123, "scenario": "low", "reward": 3672.768879674375, "avg_cost": 0.03935840517761082, "steps": 3600},
        {"episode": 124, "scenario": "medium", "reward": 3647.453017670661, "avg_cost": 0.04352276799049125, "steps": 3600},
        {"episode": 125, "scenario": "high", "reward": 3680.6412997990847, "avg_cost": 0.04158887958451588, "steps": 3600},
        {"episode": 126, "scenario": "low", "reward": 3712.79425445199, "avg_cost": 0.03741174817124071, "steps": 3600},
        {"episode": 127, "scenario": "medium", "reward": 3685.8866006881, "avg_cost": 0.0390914257007858, "steps": 3600},
        {"episode": 128, "scenario": "high", "reward": 3684.318260745611, "avg_cost": 0.04047212443146337, "steps": 3600},
        {"episode": 129, "scenario": "low", "reward": 3682.0417254362255, "avg_cost": 0.040155726913621445, "steps": 3600},
        {"episode": 130, "scenario": "medium", "reward": 3672.5146928951144, "avg_cost": 0.04143737520569832, "steps": 3600},
        {"episode": 131, "scenario": "high", "reward": 3697.5711576491594, "avg_cost": 0.039303715721341885, "steps": 3600},
        {"episode": 132, "scenario": "low", "reward": 3665.2667315527797, "avg_cost": 0.04119284276643561, "steps": 3600},
        {"episode": 133, "scenario": "medium", "reward": 3680.9928903207183, "avg_cost": 0.038860750229537694, "steps": 3600},
        {"episode": 134, "scenario": "high", "reward": 3677.239356994629, "avg_cost": 0.040602512450940494, "steps": 3600},
        {"episode": 135, "scenario": "low", "reward": 3609.8634686861187, "avg_cost": 0.04439335800280484, "steps": 3600},
        {"episode": 136, "scenario": "medium", "reward": 3692.762922756374, "avg_cost": 0.04167688271884496, "steps": 3600},
        {"episode": 137, "scenario": "high", "reward": 3645.530461343471, "avg_cost": 0.04398012149768571, "steps": 3600},
        {"episode": 138, "scenario": "low", "reward": 3619.962940841913, "avg_cost": 0.04342704664611827, "steps": 3600},
        {"episode": 139, "scenario": "medium", "reward": 3613.2815713203745, "avg_cost": 0.047719663873884, "steps": 3600},
        {"episode": 140, "scenario": "high", "reward": 3728.7013429924846, "avg_cost": 0.041335806801863426, "steps": 3600},
        {"episode": 141, "scenario": "low", "reward": 3693.712409036234, "avg_cost": 0.03868175616190355, "steps": 3600},
        {"episode": 142, "scenario": "medium", "reward": 3694.401074225083, "avg_cost": 0.040320378340159856, "steps": 3600},
        {"episode": 143, "scenario": "high", "reward": 3655.4610863626003, "avg_cost": 0.040453680728743266, "steps": 3600},
        {"episode": 144, "scenario": "low", "reward": 3636.080946901813, "avg_cost": 0.043288045113181906, "steps": 3600},
        {"episode": 145, "scenario": "medium", "reward": 3606.936365056783, "avg_cost": 0.04501736241069415, "steps": 3600},
        {"episode": 146, "scenario": "high", "reward": 3642.08905839175, "avg_cost": 0.04168607613498655, "steps": 3600},
        {"episode": 147, "scenario": "low", "reward": 3641.98043711856, "avg_cost": 0.040206258637157995, "steps": 3600},
        {"episode": 148, "scenario": "medium", "reward": 3634.0682510770857, "avg_cost": 0.04283308199994887, "steps": 3600},
        {"episode": 149, "scenario": "high", "reward": 3643.2824917063117, "avg_cost": 0.04184219500282779, "steps": 3600},
        {"episode": 150, "scenario": "low", "reward": 3675.4333900325, "avg_cost": 0.04152736236263688, "steps": 3600},
        {"episode": 151, "scenario": "medium", "reward": 3603.289687100798, "avg_cost": 0.04617864321315816, "steps": 3600},
        {"episode": 152, "scenario": "high", "reward": 3654.215438026935, "avg_cost": 0.04259131181247843, "steps": 3600},
        {"episode": 153, "scenario": "low", "reward": 3662.300074927509, "avg_cost": 0.040670972063801145, "steps": 3600},
        {"episode": 154, "scenario": "medium", "reward": 3653.5272852834314, "avg_cost": 0.041458162448640604, "steps": 3600},
        {"episode": 155, "scenario": "high", "reward": 3626.7782639972866, "avg_cost": 0.046800539559012075, "steps": 3600},
        {"episode": 156, "scenario": "low", "reward": 3641.800161242485, "avg_cost": 0.041891140194946073, "steps": 3600},
        {"episode": 157, "scenario": "medium", "reward": 3652.6120922751725, "avg_cost": 0.042835407950397995, "steps": 3600},
        {"episode": 158, "scenario": "high", "reward": 3648.0833821445704, "avg_cost": 0.04343369240135265, "steps": 3600},
        {"episode": 159, "scenario": "low", "reward": 3626.2843854017556, "avg_cost": 0.041052731808352595, "steps": 3600},
        {"episode": 160, "scenario": "medium", "reward": 3668.3551009194925, "avg_cost": 0.03909750649692594, "steps": 3600},
        {"episode": 161, "scenario": "high", "reward": 3678.6789788063616, "avg_cost": 0.043140079729233144, "steps": 3600},
        {"episode": 162, "scenario": "low", "reward": 3672.752401687205, "avg_cost": 0.042328769523236484, "steps": 3600},
        {"episode": 163, "scenario": "medium", "reward": 3656.6042250003666, "avg_cost": 0.04329852744134971, "steps": 3600},
        {"episode": 164, "scenario": "high", "reward": 3669.9014329761267, "avg_cost": 0.04167679009894427, "steps": 3600},
        {"episode": 165, "scenario": "low", "reward": 3615.088509912137, "avg_cost": 0.04583157107492702, "steps": 3600},
        {"episode": 166, "scenario": "medium", "reward": 3667.6012497879565, "avg_cost": 0.041445737002132874, "steps": 3600},
        {"episode": 167, "scenario": "high", "reward": 3672.1672714315355, "avg_cost": 0.04103931686873289, "steps": 3600},
        {"episode": 168, "scenario": "low", "reward": 3638.1237166896462, "avg_cost": 0.044302313718298035, "steps": 3600},
        {"episode": 169, "scenario": "medium", "reward": 3641.7575150877237, "avg_cost": 0.04646128341025259, "steps": 3600},
        {"episode": 170, "scenario": "high", "reward": 3629.523761322722, "avg_cost": 0.046084482131732836, "steps": 3600},
        {"episode": 171, "scenario": "low", "reward": 3610.9091658890247, "avg_cost": 0.042969048958815016, "steps": 3600},
        {"episode": 172, "scenario": "medium", "reward": 3599.4029051065445, "avg_cost": 0.04466363119129609, "steps": 3600},
        {"episode": 173, "scenario": "high", "reward": 3654.1261398121715, "avg_cost": 0.04518786024897256, "steps": 3600},
        {"episode": 174, "scenario": "low", "reward": 3653.866222154349, "avg_cost": 0.0453034037980251, "steps": 3600},
        {"episode": 175, "scenario": "medium", "reward": 3628.634595863521, "avg_cost": 0.04512511648354121, "steps": 3600},
        {"episode": 176, "scenario": "high", "reward": 3699.8257035799325, "avg_cost": 0.03875399794817592, "steps": 3600},
        {"episode": 177, "scenario": "low", "reward": 3640.2392012113705, "avg_cost": 0.04417987196848521, "steps": 3600},
        {"episode": 178, "scenario": "medium", "reward": 3719.879989735782, "avg_cost": 0.03922052518859143, "steps": 3600},
        {"episode": 179, "scenario": "high", "reward": 3682.8060377053916, "avg_cost": 0.04404872252890426, "steps": 3600},
        {"episode": 180, "scenario": "low", "reward": 3650.6623566728085, "avg_cost": 0.0411430677587244, "steps": 3600},
        {"episode": 181, "scenario": "medium", "reward": 3666.3214616701007, "avg_cost": 0.044968726020177, "steps": 3600},
        {"episode": 182, "scenario": "high", "reward": 3644.1525631286204, "avg_cost": 0.044922861212528205, "steps": 3600},
        {"episode": 183, "scenario": "low", "reward": 3683.1698192320764, "avg_cost": 0.04110436592742594, "steps": 3600},
        {"episode": 184, "scenario": "medium", "reward": 3648.891001395881, "avg_cost": 0.04402170914833227, "steps": 3600},
        {"episode": 185, "scenario": "high", "reward": 3648.450743302703, "avg_cost": 0.04234911450805763, "steps": 3600},
        {"episode": 186, "scenario": "low", "reward": 3641.7323381081223, "avg_cost": 0.04128313635437129, "steps": 3600},
        {"episode": 187, "scenario": "medium", "reward": 3658.840078830719, "avg_cost": 0.040840378143928116, "steps": 3600},
        {"episode": 188, "scenario": "high", "reward": 3632.882290545851, "avg_cost": 0.0433472849279254, "steps": 3600},
        {"episode": 189, "scenario": "low", "reward": 3680.4765398753807, "avg_cost": 0.041650217833488976, "steps": 3600},
        {"episode": 190, "scenario": "medium", "reward": 3594.28055838868, "avg_cost": 0.04829336574430474, "steps": 3600},
        {"episode": 191, "scenario": "high", "reward": 3700.4254432991147, "avg_cost": 0.04083101593287817, "steps": 3600},
        {"episode": 192, "scenario": "low", "reward": 3716.4686277620494, "avg_cost": 0.03918720928602852, "steps": 3600},
        {"episode": 193, "scenario": "medium", "reward": 3662.134280652739, "avg_cost": 0.044555957262507745, "steps": 3600},
        {"episode": 194, "scenario": "high", "reward": 3692.13186109066, "avg_cost": 0.04144767069490626, "steps": 3600},
        {"episode": 195, "scenario": "low", "reward": 3656.8649618700147, "avg_cost": 0.042980875181642154, "steps": 3600},
        {"episode": 196, "scenario": "medium", "reward": 3631.5106116523966, "avg_cost": 0.046904018920872155, "steps": 3600},
        {"episode": 197, "scenario": "high", "reward": 3597.292873762548, "avg_cost": 0.04908437695955702, "steps": 3600},
        {"episode": 198, "scenario": "low", "reward": 3673.4302924387157, "avg_cost": 0.04310041694740196, "steps": 3600},
        {"episode": 199, "scenario": "medium", "reward": 3676.209734380245, "avg_cost": 0.04234963674951966, "steps": 3600},
        {"episode": 200, "scenario": "high", "reward": 3668.7031519478187, "avg_cost": 0.04302932136782652, "steps": 3600}
    ],
    "best_reward": 3728.7013429924846,
    "best_episode": 140
  };

  const baselineData = [
    {method: "Fixed-Time", reward: 3402.23, cost: 0.0694},
    {method: "Actuated", reward: 3425.46, cost: 0.0680},
    {method: "Your Method", reward: 3656.28, cost: 0.0415}
  ];

  // Calculate statistics
  const stats = useMemo(() => {
    const filtered = selectedScenario === 'all' 
      ? metricsData.episodes 
      : metricsData.episodes.filter(ep => ep.scenario === selectedScenario);
    
    const rewards = filtered.map(ep => ep.reward);
    const costs = filtered.map(ep => ep.avg_cost);
    
    const avgReward = rewards.reduce((a, b) => a + b, 0) / rewards.length;
    const avgCost = costs.reduce((a, b) => a + b, 0) / costs.length;
    const maxReward = Math.max(...rewards);
    const minCost = Math.min(...costs);
    
    return { avgReward, avgCost, maxReward, minCost, count: filtered.length };
  }, [selectedScenario]);

  // Prepare data for waiting time vs global step
  const waitingTimeData = useMemo(() => {
    return metricsData.episodes.map(ep => ({
      step: ep.episode * ep.steps,
      waitingTime: ep.avg_cost,
      scenario: ep.scenario,
      episode: ep.episode
    }));
  }, []);

  // Calculate error bars for groups of 10 episodes
  const errorBarData = useMemo(() => {
    const groups = [];
    for (let i = 0; i < 200; i += 10) {
      const group = metricsData.episodes.slice(i, i + 10);
      const costs = group.map(ep => ep.avg_cost);
      const mean = costs.reduce((a, b) => a + b, 0) / costs.length;
      const std = Math.sqrt(costs.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / costs.length);
      
      groups.push({
        episodeGroup: `${i + 1}-${i + 10}`,
        episodes: i + 5,
        mean: mean,
        error: std
      });
    }
    return groups;
  }, []);

  // Prepare rolling average data
  const rollingAvgData = useMemo(() => {
    const windowSize = 10;
    return metricsData.episodes.map((ep, idx) => {
      const start = Math.max(0, idx - windowSize + 1);
      const window = metricsData.episodes.slice(start, idx + 1);
      const avgCost = window.reduce((sum, e) => sum + e.avg_cost, 0) / window.length;
      const avgReward = window.reduce((sum, e) => sum + e.reward, 0) / window.length;
      
      return {
        episode: ep.episode,
        avgCost,
        avgReward,
        scenario: ep.scenario
      };
    });
  }, []);

  return (
    <div className="w-full h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6 overflow-auto">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Traffic Signal Control Metrics</h1>
          <p className="text-slate-600">Deep Reinforcement Learning Performance Analysis</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600">Avg Reward</p>
                <p className="text-2xl font-bold text-blue-600">{stats.avgReward.toFixed(2)}</p>
              </div>
              <TrendingUp className="text-blue-600" size={32} />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600">Avg Cost (Wait Time)</p>
                <p className="text-2xl font-bold text-green-600">{stats.avgCost.toFixed(4)}</p>
              </div>
              <TrendingDown className="text-green-600" size={32} />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600">Best Reward</p>
                <p className="text-2xl font-bold text-purple-600">{stats.maxReward.toFixed(2)}</p>
              </div>
              <Activity className="text-purple-600" size={32} />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-600">Min Cost</p>
                <p className="text-2xl font-bold text-orange-600">{stats.minCost.toFixed(4)}</p>
              </div>
              <BarChart3 className="text-orange-600" size={32} />
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow p-4 mb-6 flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">View Type</label>
            <select 
              value={selectedView} 
              onChange={(e) => setSelectedView(e.target.value)}
              className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="overview">Overview</option>
              <option value="waittime">Waiting Time vs Steps</option>
              <option value="errorbars">Error Bars Analysis</option>
              <option value="comparison">Baseline Comparison</option>
              <option value="scenarios">By Scenario</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Filter Scenario</label>
            <select 
              value={selectedScenario} 
              onChange={(e) => setSelectedScenario(e.target.value)}
              className="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Scenarios</option>
              <option value="low">Low Traffic</option>
              <option value="medium">Medium Traffic</option>
              <option value="high">High Traffic</option>
            </select>
          </div>
        </div>

        {/* Charts */}
        {selectedView === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Reward Progress (Rolling Avg)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={rollingAvgData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="episode" stroke="#64748b" />
                  <YAxis stroke="#64748b" domain={[3550, 3750]} />
                  <Tooltip contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}} />
                  <Legend />
                  <Line type="monotone" dataKey="avgReward" stroke="#3b82f6" strokeWidth={2} dot={false} name="Reward" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Cost Progress (Rolling Avg)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={rollingAvgData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="episode" stroke="#64748b" />
                  <YAxis stroke="#64748b" domain={[0.03, 0.052]} />
                  <Tooltip contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}} />
                  <Legend />
                  <Line type="monotone" dataKey="avgCost" stroke="#10b981" strokeWidth={2} dot={false} name="Avg Cost" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {selectedView === 'waittime' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Waiting Time vs Global Step</h3>
            <ResponsiveContainer width="100%" height={500}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="step" 
                  name="Global Step" 
                  stroke="#64748b"
                  label={{ value: 'Global Step', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  dataKey="waitingTime" 
                  name="Waiting Time" 
                  stroke="#64748b"
                  label={{ value: 'Avg Waiting Time (Cost)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}}
                  formatter={(value, name) => [typeof value === 'number' ? value.toFixed(4) : value, name]}
                />
                <Legend />
                <Scatter 
                  name="Low Traffic" 
                  data={waitingTimeData.filter(d => d.scenario === 'low')} 
                  fill="#3b82f6" 
                />
                <Scatter 
                  name="Medium Traffic" 
                  data={waitingTimeData.filter(d => d.scenario === 'medium')} 
                  fill="#f59e0b" 
                />
                <Scatter 
                  name="High Traffic" 
                  data={waitingTimeData.filter(d => d.scenario === 'high')} 
                  fill="#ef4444" 
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'errorbars' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Error Bars Analysis (Groups of 10 Episodes)</h3>
            <ResponsiveContainer width="100%" height={500}>
              <LineChart data={errorBarData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="episodes" 
                  stroke="#64748b"
                  label={{ value: 'Episode', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  stroke="#64748b"
                  label={{ value: 'Mean Waiting Time', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}}
                  formatter={(value) => typeof value === 'number' ? value.toFixed(4) : value}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="mean" 
                  stroke="#8b5cf6" 
                  strokeWidth={2}
                  name="Mean Waiting Time"
                >
                  <ErrorBar dataKey="error" stroke="#8b5cf6" strokeWidth={1.5} />
                </Line>
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {selectedView === 'comparison' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-4">Baseline Method Comparison</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={baselineData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="method" stroke="#64748b" />
                  <YAxis stroke="#64748b" domain={[3300, 3700]} />
                  <Tooltip contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}} />
                  <Legend />
                  <Bar dataKey="reward" fill="#3b82f6" name="Average Reward" />
                </BarChart>
              </ResponsiveContainer>

              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={baselineData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="method" stroke="#64748b" />
                  <YAxis stroke="#64748b" domain={[0, 0.08]} />
                  <Tooltip contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff'}} />
                  <Legend />
                  <Bar dataKey="cost" fill="#10b981" name="Average Cost" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-slate-700">
                <strong>Performance Improvement:</strong> Your method shows a 
                <span className="text-blue-600 font-semibold"> {((stats.avgReward - 3425.46) / 3425.46 * 100).toFixed(2)}%</span> increase in reward and a
                <span className="text-green-600 font-semibold"> {((0.0680 - stats.avgCost) / 0.0680 * 100).toFixed(2)}%</span> reduction in waiting time compared to Actuated baseline.
              </p>
            </div>
          </div>
        )}

        {selectedView === 'scenarios' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {['low', 'medium', 'high'].map(scenario => {
              const scenarioData = metricsData.episodes.filter(ep => ep.scenario === scenario);
              const avgCost = scenarioData.reduce((sum, ep) => sum + ep.avg_cost, 0) / scenarioData.length;
              const avgReward = scenarioData.reduce((sum, ep) => sum + ep.reward, 0) / scenarioData.length;
              
              return (
                <div key={scenario} className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-semibold text-slate-800 mb-4 capitalize">{scenario} Traffic</h3>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-slate-600">Avg Reward</p>
                      <p className="text-xl font-bold text-blue-600">{avgReward.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-600">Avg Cost</p>
                      <p className="text-xl font-bold text-green-600">{avgCost.toFixed(4)}</p>
                    </div>
                    <ResponsiveContainer width="100%" height={200}>
                      <LineChart data={scenarioData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                        <XAxis dataKey="episode" stroke="#64748b" fontSize={10} />
                        <YAxis stroke="#64748b" fontSize={10} domain={[0.03, 0.055]} />
                        <Tooltip contentStyle={{backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px'}} />
                        <Line type="monotone" dataKey="avg_cost" stroke="#10b981" strokeWidth={2} dot={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default TrafficMetricsVisualization;
