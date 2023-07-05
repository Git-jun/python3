# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_cdn20180510 import models as cdn_20180510_models
from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_cdn20180510.models import RefreshObjectCachesRequest
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Cdn20180510Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Cdn
        config.endpoint = f'cdn.aliyuncs.com'
        return Cdn20180510Client(config)

    @staticmethod
    def main(args: List[str]) -> None:
        # 创建CDN客户端
        client = Sample.create_client(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])

        # 域名列表
        domain_list = [
            'https://www.minefi.io/',
            'https://minefi.io/'
        ]

        for domain in domain_list:
            # 构造刷新请求对象
            refresh_request = cdn_20180510_models.RefreshObjectCachesRequest(
                object_path=domain,  # 要刷新的URL
                object_type='Directory',  # 刷新类型，可选值为'File'或'Directory'
                security_token='your_value'  # 可选，安全令牌
            )

            try:
                # 调用刷新接口
                response = client.refresh_object_caches(refresh_request)

                # 处理刷新结果
                print(f"刷新成功: {domain}")
            except Exception as error:
                print(f"刷新失败: {domain}，错误信息: {error}")


if __name__ == '__main__':
    Sample.main(sys.argv[1:])

