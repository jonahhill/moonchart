# Copyright 2019 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To run: python3 -m unittest discover -s tests/ -p test_*.py -t . -v

import os
import unittest
import pandas as pd
# Specify non-interactive matplotlib backend before anything else imports
# matplotlib
import matplotlib as mpl
mpl.use("Agg")
from moonchart import DailyPerformance, AggregateDailyPerformance
from moonchart.utils import get_zscores

BACKTEST_RESULTS = {
    'strategy-1': {
        ('AbsExposure', '2018-12-03'): 0.333333333,
        ('AbsExposure', '2018-12-04'): 0.333333333,
        ('AbsExposure', '2018-12-05'): 0.333333333,
        ('AbsWeight', '2018-12-03'): 0.333333333,
        ('AbsWeight', '2018-12-04'): 0.333333333,
        ('AbsWeight', '2018-12-05'): 0.333333333,
        ('Commission', '2018-12-03'): 0.0001,
        ('Commission', '2018-12-04'): 0.0001,
        ('Commission', '2018-12-05'): 0.0001,
        ('NetExposure', '2018-12-03'): -0.03030303,
        ('NetExposure', '2018-12-04'): 0.060606060999999996,
        ('NetExposure', '2018-12-05'): -0.090909091,
        ('Return', '2018-12-03'): -0.002257125,
        ('Return', '2018-12-04'): -0.000375271,
        ('Return', '2018-12-05'): -0.002395708,
        ('TotalHoldings', '2018-12-03'): 22.0,
        ('TotalHoldings', '2018-12-04'): 22.0,
        ('TotalHoldings', '2018-12-05'): 22.0,
        ('Trade', '2018-12-03'): 0.049062049,
        ('Trade', '2018-12-04'): 0.090909091,
        ('Trade', '2018-12-05'): -0.151515152},
    'strategy-2': {
        ('AbsExposure', '2018-12-03'): 0.333333333,
        ('AbsExposure', '2018-12-04'): 0.333333333,
        ('AbsExposure', '2018-12-05'): 0.333333333,
        ('AbsWeight', '2018-12-03'): 0.333333333,
        ('AbsWeight', '2018-12-04'): 0.333333333,
        ('AbsWeight', '2018-12-05'): 0.333333333,
        ('Commission', '2018-12-03'): 0.0,
        ('Commission', '2018-12-04'): 0.0,
        ('Commission', '2018-12-05'): 0.0,
        ('NetExposure', '2018-12-03'): 0.333333333,
        ('NetExposure', '2018-12-04'): 0.333333333,
        ('NetExposure', '2018-12-05'): 0.333333333,
        ('Return', '2018-12-03'): 0.00278717,
        ('Return', '2018-12-04'): -0.005031677,
        ('Return', '2018-12-05'): -0.004845368,
        ('TotalHoldings', '2018-12-03'): 25.0,
        ('TotalHoldings', '2018-12-04'): 25.0,
        ('TotalHoldings', '2018-12-05'): 25.0,
        ('Trade', '2018-12-03'): -3.47e-18,
        ('Trade', '2018-12-04'): 0.0,
        ('Trade', '2018-12-05'): 0.0}}

PNL_RESULTS = {
    'strategy-a': {
        ('AbsExposure', '2019-01-21 23:59:59'): '0',
        ('AbsExposure', '2019-01-22 23:59:59'): '0',
        ('AbsExposure', '2019-01-23 23:59:59'): '0',
        ('Account', '2019-01-21 23:59:59'): 'U12345',
        ('Account', '2019-01-22 23:59:59'): 'U12345',
        ('Account', '2019-01-23 23:59:59'): 'U12345',
        ('Commission', '2019-01-21 23:59:59'): '0',
        ('Commission', '2019-01-22 23:59:59'): '2.54E-05',
        ('Commission', '2019-01-23 23:59:59'): '7.11E-05',
        ('CommissionAmount', '2019-01-21 23:59:59'): '0',
        ('CommissionAmount', '2019-01-22 23:59:59'): '15.3382',
        ('CommissionAmount', '2019-01-23 23:59:59'): '43.691',
        ('NetExposure', '2019-01-21 23:59:59'): '0',
        ('NetExposure', '2019-01-22 23:59:59'): '0',
        ('NetExposure', '2019-01-23 23:59:59'): '0',
        ('NetLiquidation', '2019-01-21 23:59:59'): '604431.98',
        ('NetLiquidation', '2019-01-22 23:59:59'): '604346.46',
        ('NetLiquidation', '2019-01-23 23:59:59'): '614640.04',
        ('OrderRef', '2019-01-21 23:59:59'): 'strategy-a',
        ('OrderRef', '2019-01-22 23:59:59'): 'strategy-a',
        ('OrderRef', '2019-01-23 23:59:59'): 'strategy-a',
        ('Pnl', '2019-01-21 23:59:59'): '0',
        ('Pnl', '2019-01-22 23:59:59'): '732.6318',
        ('Pnl', '2019-01-23 23:59:59'): '2463.289',
        ('Return', '2019-01-21 23:59:59'): '0',
        ('Return', '2019-01-22 23:59:59'): '0.00121226',
        ('Return', '2019-01-23 23:59:59'): '0.00400769'},
    'strategy-b': {
        ('AbsExposure', '2019-01-21 23:59:59'): '0',
        ('AbsExposure', '2019-01-22 23:59:59'): '0',
        ('AbsExposure', '2019-01-23 23:59:59'): '0',
        ('Account', '2019-01-21 23:59:59'): 'U12345',
        ('Account', '2019-01-22 23:59:59'): 'U12345',
        ('Account', '2019-01-23 23:59:59'): 'U12345',
        ('Commission', '2019-01-21 23:59:59'): '0',
        ('Commission', '2019-01-22 23:59:59'): '0.000179206',
        ('Commission', '2019-01-23 23:59:59'): '5.55E-05',
        ('CommissionAmount', '2019-01-21 23:59:59'): '0',
        ('CommissionAmount', '2019-01-22 23:59:59'): '108.3024',
        ('CommissionAmount', '2019-01-23 23:59:59'): '34.0915',
        ('NetExposure', '2019-01-21 23:59:59'): '0',
        ('NetExposure', '2019-01-22 23:59:59'): '0',
        ('NetExposure', '2019-01-23 23:59:59'): '0',
        ('NetLiquidation', '2019-01-21 23:59:59'): '604431.98',
        ('NetLiquidation', '2019-01-22 23:59:59'): '604346.46',
        ('NetLiquidation', '2019-01-23 23:59:59'): '614640.04',
        ('OrderRef', '2019-01-21 23:59:59'): 'strategy-b',
        ('OrderRef', '2019-01-22 23:59:59'): 'strategy-b',
        ('OrderRef', '2019-01-23 23:59:59'): 'strategy-b',
        ('Pnl', '2019-01-21 23:59:59'): '0',
        ('Pnl', '2019-01-22 23:59:59'): '501.1911',
        ('Pnl', '2019-01-23 23:59:59'): '6534.1285',
        ('Return', '2019-01-21 23:59:59'): '0',
        ('Return', '2019-01-22 23:59:59'): '0.0008293',
        ('Return', '2019-01-23 23:59:59'): '0.01063083'}}

class DailyPerformanceTestCase(unittest.TestCase):
    """
    Test cases for DailyPerformance and AggregateDailyPerformance.
    """

    def setUp(self):
        """
        Write test fixtures to CSV.
        """
        backtest_results = pd.DataFrame.from_dict(BACKTEST_RESULTS)
        backtest_results.index.set_names(["Field","Date"], inplace=True)
        backtest_results.to_csv("backtest.csv")

        pnl_results = pd.DataFrame.from_dict(PNL_RESULTS)
        pnl_results.index.set_names(["Field","Date"], inplace=True)
        pnl_results.to_csv("pnl.csv")

    def tearDown(self):
        """
        Remove files.
        """
        os.remove("backtest.csv")
        os.remove("pnl.csv")

    def test_from_moonshot_csv(self):

        perf = DailyPerformance.from_moonshot_csv("backtest.csv")
        self.assertListEqual(
            list(perf.returns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05']
        )
        self.assertDictEqual(
            perf.returns.to_dict(orient="list"),
            {'strategy-1': [-0.002257125, -0.000375271, -0.002395708],
             'strategy-2': [0.00278717, -0.005031677, -0.004845368]})

        self.assertListEqual(
            list(perf.abs_exposures.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.abs_exposures.to_dict(orient="list"),
            {'strategy-1': [0.333333333, 0.333333333, 0.333333333],
             'strategy-2': [0.333333333, 0.333333333, 0.333333333]})

        self.assertListEqual(
            list(perf.net_exposures.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.net_exposures.to_dict(orient="list"),
            {'strategy-1': [-0.03030303, 0.060606061, -0.090909091],
             'strategy-2': [0.333333333, 0.333333333, 0.333333333]})

        self.assertListEqual(
            list(perf.trades.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.trades.to_dict(orient="list"),
            {'strategy-1': [0.049062049, 0.090909091, -0.151515152],
             'strategy-2': [-3.47e-18, 0.0, 0.0]})

        self.assertListEqual(
            list(perf.total_holdings.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.total_holdings.to_dict(orient="list"),
            {'strategy-1': [22.0, 22.0, 22.0], 'strategy-2': [25.0, 25.0, 25.0]})

        self.assertListEqual(
            list(perf.commissions_pct.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.commissions_pct.to_dict(orient="list"),
            {'strategy-1': [0.0001, 0.0001, 0.0001], 'strategy-2': [0.0, 0.0, 0.0]})

        self.assertDictEqual(
            perf.cagr.to_dict(),
            {'strategy-1': -0.6009354029100387, 'strategy-2': -0.7272165531290371})

        self.assertDictEqual(
            perf.sharpe.to_dict(),
            {'strategy-1': -23.574049805803934, 'strategy-2': -8.409034049060317}
        )

        self.assertListEqual(
            list(perf.cum_returns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.cum_returns.to_dict(orient="list"),
            {'strategy-1': [0.997742875, 0.9973684510335559, 0.9949790474564671],
             'strategy-2': [1.00278717, 0.9977414688608159, 0.9929070442753247]}
        )

        self.assertListEqual(
            list(perf.drawdowns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertDictEqual(
            perf.drawdowns.to_dict(orient="list"),
            {'strategy-1': [0.0, -0.00037527100000001035, -0.0027700799602632387],
             'strategy-2': [0.0, -0.005031676999999957, -0.009852664673277833]}
        )

        self.assertDictEqual(
            perf.max_drawdown.to_dict(),
            {'strategy-1': -0.0027700799602632387, 'strategy-2': -0.009852664673277833})

    def test_from_moonshot_csv_agg_perf(self):

        perf = DailyPerformance.from_moonshot_csv("backtest.csv")
        agg_perf = AggregateDailyPerformance(perf)

        self.assertListEqual(
            list(agg_perf.returns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05']
        )
        self.assertListEqual(
            agg_perf.returns.tolist(),
            [0.0005300449999999998, -0.005406948, -0.007241076])

        self.assertListEqual(
            list(agg_perf.abs_exposures.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.abs_exposures.tolist(),
            [0.666666666, 0.666666666, 0.666666666])

        self.assertListEqual(
            list(agg_perf.net_exposures.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.net_exposures.tolist(),
            [0.303030303, 0.393939394, 0.242424242])

        self.assertListEqual(
            list(agg_perf.trades.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.trades.tolist(),
            [0.049062048999999996, 0.090909091, -0.151515152])

        self.assertListEqual(
            list(agg_perf.total_holdings.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.total_holdings.tolist(),
            [47.0, 47.0, 47.0])

        self.assertListEqual(
            list(agg_perf.commissions_pct.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.commissions_pct.tolist(),
            [0.0001, 0.0001, 0.0001])

        self.assertEqual(
            agg_perf.cagr,-0.8912867832023363)

        self.assertEqual(
            agg_perf.sharpe, -15.785645344093775)

        self.assertListEqual(
            list(agg_perf.cum_returns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.cum_returns.tolist(),
            [1.000530045, 0.9951202310742474, 0.9879144898519012])

        self.assertListEqual(
            list(agg_perf.drawdowns.index.strftime("%Y-%m-%d")),
            ['2018-12-03', '2018-12-04', '2018-12-05'])

        self.assertListEqual(
            agg_perf.drawdowns.tolist(),
            [0.0, -0.005406947999999967, -0.012608871878603933]
        )

        self.assertEqual(
            agg_perf.max_drawdown, -0.012608871878603933)

    def test_from_pnl_csv(self):

        perf = DailyPerformance.from_pnl_csv("pnl.csv")
        self.assertListEqual(
            list(perf.returns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59']
        )
        self.assertDictEqual(
            perf.returns.to_dict(orient="list"),
            {'strategy-a': [0.0, 0.00121226, 0.00400769],
             'strategy-b': [0.0, 0.0008293, 0.01063083]})

        self.assertListEqual(
            list(perf.abs_exposures.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.abs_exposures.to_dict(orient="list"),
            {'strategy-a': [0.0, 0.0, 0.0], 'strategy-b': [0.0, 0.0, 0.0]})

        self.assertListEqual(
            list(perf.pnl.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.pnl.to_dict(orient="list"),
            {'strategy-a': [0.0, 732.6318, 2463.289],
             'strategy-b': [0.0, 501.1911, 6534.1285]})

        self.assertListEqual(
            list(perf.commissions.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.commissions.to_dict(orient="list"),
            {'strategy-a': [0.0, 15.3382, 43.691], 'strategy-b': [0.0, 108.3024, 34.0915]})

        self.assertListEqual(
            list(perf.cum_pnl.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.cum_pnl.to_dict(orient="list"),
           {'strategy-a': [0.0, 732.6318, 3195.9208000000003],
            'strategy-b': [0.0, 501.1911, 7035.3196]})

        self.assertListEqual(
            list(perf.commissions_pct.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.commissions_pct.to_dict(orient="list"),
            {'strategy-a': [0.0, 2.54e-05, 7.11e-05],
             'strategy-b': [0.0, 0.000179206, 5.55e-05]})

        self.assertDictEqual(
            perf.cagr.to_dict(),
            {'strategy-a': 1.5884135772875698, 'strategy-b': 7.013847123487736})

        self.assertDictEqual(
            perf.sharpe.to_dict(),
            {'strategy-a': 13.439089525191742, 'strategy-b': 10.255814111748151}
        )

        self.assertListEqual(
            list(perf.cum_returns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.cum_returns.to_dict(orient="list"),
            {'strategy-a': [1.0, 1.00121226, 1.0052248083622792],
             'strategy-b': [1.0, 1.0008293, 1.011468946147319]}
        )

        self.assertListEqual(
            list(perf.drawdowns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertDictEqual(
            perf.drawdowns.to_dict(orient="list"),
            {'strategy-a': [0.0, 0.0, 0.0], 'strategy-b': [0.0, 0.0, 0.0]})

        self.assertDictEqual(
            perf.max_drawdown.to_dict(),
            {'strategy-a': 0.0, 'strategy-b': 0.0})

    def test_from_pnl_csv_agg_perf(self):

        perf = DailyPerformance.from_pnl_csv("pnl.csv")
        agg_perf = AggregateDailyPerformance(perf)

        self.assertListEqual(
            list(agg_perf.returns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59']
        )
        self.assertListEqual(
            agg_perf.returns.tolist(),
            [0.0, 0.00204156, 0.014638520000000002])

        self.assertListEqual(
            list(agg_perf.abs_exposures.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.abs_exposures.tolist(),
            [0.0, 0.0, 0.0])

        self.assertListEqual(
            list(agg_perf.pnl.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.pnl.tolist(),
            [0.0, 1233.8229000000001, 8997.4175])

        self.assertListEqual(
            list(agg_perf.commissions.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.commissions.tolist(),
            [0.0, 123.6406, 77.7825])

        self.assertListEqual(
            list(agg_perf.cum_pnl.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.cum_pnl.tolist(),
           [0.0, 1233.8229000000001, 10231.240399999999])

        self.assertListEqual(
            list(agg_perf.commissions_pct.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.commissions_pct.tolist(),
            [0.0, 0.000204606, 0.0001266])

        self.assertEqual(
            agg_perf.cagr, 19.581032951701545)

        self.assertEqual(
            agg_perf.sharpe, 11.132759642908027)

        self.assertListEqual(
            list(agg_perf.cum_returns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.cum_returns.tolist(),
            [1.0, 1.00204156, 1.0167099654168914]
        )

        self.assertListEqual(
            list(agg_perf.drawdowns.index.strftime("%Y-%m-%d %H:%M:%S")),
            ['2019-01-21 23:59:59', '2019-01-22 23:59:59', '2019-01-23 23:59:59'])

        self.assertListEqual(
            agg_perf.drawdowns.tolist(),
            [0.0, 0.0, 0.0])

        self.assertEqual(
            agg_perf.max_drawdown, 0.0)

    def test_riskfree(self):

        perf = DailyPerformance.from_pnl_csv("pnl.csv")
        self.assertDictEqual(
            perf.sharpe.to_dict(),
            {'strategy-a': 13.439089525191742, 'strategy-b': 10.255814111748151}
        )

        perf = DailyPerformance.from_pnl_csv("pnl.csv", riskfree=0.02/252)
        self.assertDictEqual(
            perf.sharpe.to_dict(),
            {'strategy-a': 12.826098362386784, 'strategy-b': 10.04273969611786}
        )

    def test_compound(self):

        perf = DailyPerformance.from_moonshot_csv("backtest.csv")
        self.assertDictEqual(
            perf.cum_returns.to_dict(orient="list"),
            {'strategy-1': [0.997742875, 0.9973684510335559, 0.9949790474564671],
             'strategy-2': [1.00278717, 0.9977414688608159, 0.9929070442753247]}
        )

        perf = DailyPerformance.from_moonshot_csv("backtest.csv", compound=False)
        self.assertDictEqual(
            perf.cum_returns.to_dict(orient="list"),
            {'strategy-1': [0.997742875, 0.997367604, 0.994971896],
             'strategy-2': [1.00278717, 0.997755493, 0.992910125]}
        )

    def test_rolling_sharpe_window(self):

        perf = DailyPerformance.from_moonshot_csv("backtest.csv")
        self.assertDictEqual(
            perf.rolling_sharpe.fillna(-1).to_dict(orient="list"),
            {'strategy-1': [-1.0, -1.0, -1.0],
             'strategy-2': [-1.0, -1.0, -1.0]}
        )

        perf = DailyPerformance.from_moonshot_csv("backtest.csv", rolling_sharpe_window=2)
        self.assertDictEqual(
            perf.rolling_sharpe.fillna(-1).to_dict(orient="list"),
            {'strategy-1': [-1.0, -22.205756137004837, -21.77149197579271],
             'strategy-2': [-1.0, -4.55699466016689, -841.576244567701]}
        )

    def test_trim_outliers(self):

        perf = DailyPerformance.from_moonshot_csv("backtest.csv")
        zscores = get_zscores(perf.returns)

        self.assertDictEqual(
            zscores.to_dict(orient="list"),
            {'strategy-1': [-0.5148664345304096, 1.152522272022025, -0.6376558374916148],
             'strategy-2': [1.1544487988426575, -0.5981044889340401, -0.5563443099086175]}
        )

        self.assertDictEqual(
            perf.returns.to_dict(orient="list"),
            {'strategy-1': [-0.002257125, -0.000375271, -0.002395708],
             'strategy-2': [0.00278717, -0.005031677, -0.004845368]}
        )

        perf = DailyPerformance.from_moonshot_csv("backtest.csv", trim_outliers=1.154)
        self.assertDictEqual(
            perf.returns.to_dict(orient="list"),
            {'strategy-1': [-0.002257125, -0.000375271, -0.002395708],
             'strategy-2': [0.0, -0.005031677, -0.004845368]}
        )
