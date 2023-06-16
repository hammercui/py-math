import argparse
import getopt
import sys


class ArgumentTools:

    @staticmethod
    def get_env():
        env = "dev"
        sd_host = 'http://127.0.0.1:7861'
        parser = argparse.ArgumentParser()
        parser.add_argument("--env", choices=['local', 'dev', 'test', 'prod'], type=str,
                            help="eg:local,dev,prod.config the runtime environment,for different .env.ini",
                            default="dev")
        if len(sys.argv) > 1:
            env = sys.argv[1]
            env = env.split("=")[1]
        print(f"\t sys.argv:{sys.argv}")
        if len(sys.argv) > 2:
            sd_host = sys.argv[2]
            sd_host = sd_host.split("=")[1]
        return env, sd_host

    @staticmethod
    def parsing_params(param_keys: []):
        params = []
        if param_keys is None:
            return params
        long_param_keys = [param_key + '=' for param_key in param_keys]
        opts, args = getopt.getopt(sys.argv[1:], "", long_param_keys)
        for param_key in param_keys:
            line_param_key = '--' + param_key
            has_value = False
            for op, value in opts:
                if op == line_param_key:
                    params.append(value)
                    has_value = True
            if not has_value:
                if 'env' == param_key:
                    params.append('dev')
                elif 'role' == param_key:
                    params.append('slave')
                elif 'region' == param_key:
                    params.append('test')

                else:
                    raise Exception(f'param: {param_key} not found.')
        if len(params) == 1:
            return params[0]
        return params