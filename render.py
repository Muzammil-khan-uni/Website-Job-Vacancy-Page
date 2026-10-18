from playwright.sync_api import sync_playwright
from pathlib import Path
from base64 import b64encode
base=Path(__file__).parent
html=(base/'index.html').read_text()
css=(base/'styles.css').read_text()
js=(base/'script.js').read_text()
img=b64encode((base/'assets/careers-3d.png').read_bytes()).decode()
html=html.replace('<link rel="stylesheet" href="styles.css" />',f'<style>{css}</style>')
html=html.replace('<script defer src="script.js"></script>','')
html=html.replace('</body>',f'<script>{js}</script></body>')
html=html.replace('src="assets/careers-3d.png"','src="data:image/png;base64,'+img+'"')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--no-proxy-server'])
    for viewport,out in [({'width':1440,'height':900},'desktop-full.png'),({'width':390,'height':844},'mobile-full.png'),({'width':768,'height':1024},'tablet-full.png')]:
        page=browser.new_page(viewport=viewport,device_scale_factor=1)
        page.set_content(html, wait_until='load')
        page.evaluate('document.fonts.ready')
        page.add_style_tag(content='*, *:before,*:after{animation:none!important;transition:none!important;}.preview-disclaimer{display:none!important;}')
        page.screenshot(path=str(base/out),full_page=True)
        print(out,page.title(),page.locator('body').evaluate('(el)=>el.scrollHeight'))
        if viewport['width']==1440:
            page.screenshot(path=str(base/'desktop-hero.png'),full_page=False)
            page.evaluate("document.querySelector('.am-site-header').style.position='static'")
            page.locator('#apply').screenshot(path=str(base/'desktop-form.png'))
            page.locator('#submit-button').click()
            print('Empty validation:',page.locator('#form-message').inner_text())
            page.locator('#applicant_type').select_option('foreigner')
            print('Passport required:',page.locator('#passport_number').get_attribute('required'))
        if viewport['width']==390:
            page.screenshot(path=str(base/'mobile-hero.png'),full_page=False)
            page.locator('.form-panel').scroll_into_view_if_needed()
            page.screenshot(path=str(base/'mobile-form.png'),full_page=False)
        if viewport['width']==768:
            page.screenshot(path=str(base/'tablet-hero.png'),full_page=False)
        page.close()
    browser.close()
