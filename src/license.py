import os
import json

import requests
from lxml import html as lh

root_url = 'https://parivahan.gov.in'
url = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'


def get_licence_status(args):
    sess = requests.Session()

    try:
        resp = sess.get(url=url)
    except requests.ConnectionError:
        print("There is a problem in network and connection to url")
        raise SystemExit()
    except requests.exceptions.RequestException as e:
        print("An ambiguous request error happened ", e)
        raise SystemExit(e)

    tree = lh.document_fromstring(resp.content)
    token_ViewState = tree.xpath("//input[@name='javax.faces.ViewState']/@value")[0]
    img_src = tree.xpath("//img[@id='form_rcdl:j_idt34:j_idt41']/@src")[0]

    try:
        image = sess.get(root_url + img_src, stream=True).content
    except requests.exceptions.RequestException as e:
        print("An ambigous request error ", e)
        raise SystemExit(e)

    file_path = os.path.join(os.path.dirname(__file__), 'captcha.jpg')
    with open(file_path, 'wb') as out_file:
        out_file.write(image)

    captchaText = get_captcha()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    data = {
        'form_rcdl': 'form_rcdl',
        'form_rcdl:tf_dlNO': args.license_no,
        'form_rcdl:tf_dob_input': args.dob,
        'form_rcdl:j_idt34:CaptchaID': captchaText,
        'javax.faces.ViewState': token_ViewState,
        'javax.faces.partial.ajax': 'true',
        'javax.faces.source': 'form_rcdl:j_idt46',
        'javax.faces.partial.execute': '@all',
        'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
        'form_rcdl:j_idt46': 'form_rcdl:j_idt46',
    }

    try:
        resp_post = sess.post(url, data=data, headers=headers)
    except requests.ConnectionError:
        print("There is a problem in network and connection to url")
        raise SystemExit()
    except requests.exceptions.RequestException as e:
        print("An ambigous request error ", e)
        raise SystemExit(e)

    if resp_post.status_code == 200:
        # print(resp_post.content)
        tree = lh.document_fromstring(resp_post.content)

        try:
            name = tree.xpath('//table[1]/tr[2]/td/text()')[0]
            issue_date = tree.xpath('//table[1]/tr[3]/td[2]/text()')[0]
            expiry_date = tree.xpath('//table[2]/tr[1]/td[3]/text()')[0]
            cov_category = tree.xpath("//div[@id='form_rcdl:j_idt167']/div/table/tbody/tr[1]/td[1]/text()")[0]
            vehicle_class = tree.xpath("//div[@id='form_rcdl:j_idt167']/div/table/tbody/tr[1]/td[2]/text()")[0]

            result = {
                'name': ' '.join(name.split()),
                'issue_date': issue_date,
                'expiry_date': expiry_date,
                'cov_category': cov_category,
                'vehicle_class': vehicle_class,
            }

            result = json.dumps(result)
            return result
        except:
            print("The input data is not correct!")


def get_captcha():
    captchaText = input('Enter the captcha: ')
    return captchaText
