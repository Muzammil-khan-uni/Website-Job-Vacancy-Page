from pathlib import Path
from playwright.sync_api import sync_playwright
from datetime import date, timedelta
from base64 import b64encode
base=Path(__file__).parent
sample=base/'test-cv.pdf'
sample.write_bytes(b'%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\n%%EOF')
html=(base/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="styles.css" />','<style>'+(base/'styles.css').read_text()+'</style>')
html=html.replace('<script defer src="script.js"></script>', '')
html=html.replace('src="assets/careers-3d.png"', 'src="data:image/png;base64,'+b64encode((base/'assets/careers-3d.png').read_bytes()).decode()+'"')
html=html.replace('</body>', '<script>'+(base/'script.js').read_text()+'</script></body>')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(1100,800),(1024,768),(768,1024),(390,844),(320,700)]:
  pg=b.new_page(viewport={'width':w,'height':h})
  errors=[]
  pg.on('pageerror', lambda e: errors.append(str(e)))
  pg.set_content(html,wait_until='load')
  pg.wait_for_timeout(150)
  geometry=pg.evaluate('({vw:document.documentElement.clientWidth,sw:document.documentElement.scrollWidth,body:document.body.scrollWidth})')
  assert not errors, f'JS errors {w}: {errors}'
  assert geometry['sw']<=w+1, f'horiz scroll @ {w}: {geometry}'
  print('viewport',w,'PASS',geometry)
  if w==390:
   menu=pg.locator('.menu-toggle');menu.click();assert pg.locator('#mobile-nav').is_visible();assert pg.locator('#mobile-nav a').count()==8
   menu.click();assert not pg.locator('#mobile-nav').is_visible()
  if w==1440:
   pg.locator('#submit-button').click();assert 'highlighted fields' in pg.locator('#form-message').inner_text()
   pg.locator('#applicant_type').select_option('foreigner')
   assert pg.locator('#passport_number').is_visible()
   assert pg.locator('#passport_number').get_attribute('required') is not None
   pg.locator('#applicant_type').select_option('malaysian')
   assert not pg.locator('#passport_number').is_visible()
   pg.locator('#full_name').fill('Test Candidate')
   pg.locator('#email').fill('candidate@example.com')
   pg.locator('#dob').fill('1997-05-20')
   pg.locator('#mobile').fill('+60 12 345 6789')
   pg.locator('#employer').fill('Test Employer')
   pg.locator('#start_date').fill((date.today()+timedelta(days=30)).isoformat())
   pg.locator('#linkedin').fill('https://www.linkedin.com/in/test-candidate')
   pg.locator('#cv').set_input_files(str(sample))
   pg.locator('#consent').check()
   pg.locator('#submit-button').click()
   result=pg.locator('#form-message').inner_text()
   print('valid preview:',result)
   assert 'pass the preview checks' in result
  pg.close()
 b.close()
sample.unlink()
print('UI tests passed')
