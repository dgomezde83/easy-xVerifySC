import unittest
from verify import main
import argparse

class TestBuildAndVerifyScript(unittest.TestCase):

    def test_command_generation_1(self):
        test_args_1 = argparse.Namespace(
            project_dir='barterswap',
            build_output_dir='verifyswap',
            image_version='v5.3.0',
            smart_contract_address='erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs',
            network='D',
            wallet='mywallet.pem'
        )

        build_command_1, mxpy_command_1 = main(test_args_1)

        self.assertIn('mxpy --verbose contract verify erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs --packaged-src=/home/dan83l/Documents/verifyswap/barterswap/barterswap-1.0.0.source.json --verifier-url=https://devnet-play-api.multiversx.com --docker-image=multiversx/sdk-rust-contract-builder:v5.3.0 --pem mywallet.pem', mxpy_command_1)

    def test_command_generation_2(self):
        test_args_2 = argparse.Namespace(
            project_dir='barterswap',
            build_output_dir='verifyswap2',
            image_version='v5.3.0',
            smart_contract_address='erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs',
            network='D',
            wallet='mywallet.json'
        )

        build_command_2, mxpy_command_2 = main(test_args_2)

        self.assertIn('mxpy --verbose contract verify erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs --packaged-src=/home/dan83l/Documents/verifyswap2/barterswap/barterswap-1.0.0.source.json --verifier-url=https://devnet-play-api.multiversx.com --docker-image=multiversx/sdk-rust-contract-builder:v5.3.0 --keyfile mywallet.json', mxpy_command_2)

    def test_command_generation_3(self):
        test_args_3 = argparse.Namespace(
            project_dir='barterswap',
            build_output_dir='verifyswap3',
            image_version='v5.3.0',
            smart_contract_address='erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs',
            network='M',
            wallet='mywallet.json'
        )

        build_command_3, mxpy_command_3 = main(test_args_3)

        self.assertIn('mxpy --verbose contract verify erd1qqqqqqqqqqqqqpgq5cfxcvq5dqp290j2q9gw5yc8fcremmlqplkqtly3rs --packaged-src=/home/dan83l/Documents/verifyswap3/barterswap/barterswap-1.0.0.source.json --verifier-url=https://play-api.multiversx.com --docker-image=multiversx/sdk-rust-contract-builder:v5.3.0 --keyfile mywallet.json', mxpy_command_3)

if __name__ == '__main__':
    unittest.main()
