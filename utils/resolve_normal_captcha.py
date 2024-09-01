from twocaptcha import TwoCaptcha

def resolve_normal_captcha(sb, seletor):
    while sb.driver.is_element_visible('input[name*="answer"]'):
        captcha_img = sb.driver.find_element(seletor)
        captcha_img.screenshot('captchas/captcha.png')
        
        CAPTCHA_KEY = 'd8be5dbaf02ed563ad5d6630a455cf75'

        solver = TwoCaptcha(CAPTCHA_KEY)
        
        try:
            result = solver.normal('captchas/captcha.png')
        except Exception as e:
            print(e)
        else:
            code = result['code']
            sb.driver.type('input[name*="answer"]', code)
            sb.driver.sleep(3)
            sb.driver.click("button#jar")