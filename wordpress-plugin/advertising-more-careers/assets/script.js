(()=>{
 const root=document.getElementById('am-careers-root'); if(!root) return;
 const $=(s)=>root.querySelector(s);
 const header=$('#site-header'),menu=$('.menu-toggle'),mobile=$('#mobile-nav');
 window.addEventListener('scroll',()=>header.classList.toggle('scrolled',window.scrollY>10),{passive:true});
 menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');mobile.hidden=!open});
 mobile?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{mobile.hidden=true;menu.setAttribute('aria-expanded','false')}));
 const form=$('#application-form'); if(!form)return;
 const applicant=$('#applicant_type'),passportWrap=$('#passport-field'),passport=$('#passport_number'),cv=$('#cv'),drop=$('#upload-zone'),fileName=$('#file-name'),msg=$('#form-message'),button=$('#submit-button');
 const today=new Date();const isoToday=[today.getFullYear(),String(today.getMonth()+1).padStart(2,'0'),String(today.getDate()).padStart(2,'0')].join('-');
 $('#dob').max=isoToday;$('#start_date').min=isoToday;$('#year').textContent=String(today.getFullYear());
 function passportState(){let isForeign=applicant.value==='foreigner';passportWrap.hidden=!isForeign;passport.required=isForeign;if(!isForeign){passport.value='';clearError(passport)}}
 applicant.addEventListener('change',passportState);passportState();
 function clearError(field){field.classList.remove('invalid');field.removeAttribute('aria-invalid');let holder=field.closest('.field');if(holder){const error=holder.querySelector('.field-error');if(error)error.textContent=''}if(field===cv)drop.classList.remove('invalid')}
 function error(field,text){field.classList.add('invalid');field.setAttribute('aria-invalid','true');let holder=field.closest('.field');if(holder){const e=holder.querySelector('.field-error');if(e)e.textContent=text}if(field===cv)drop.classList.add('invalid')}
 function validateCV(){const f=cv.files?.[0];if(!f){error(cv,'Please attach your resume or CV.');return false}if(!/\.(pdf|doc|docx)$/i.test(f.name)){error(cv,'Only PDF, DOC and DOCX files are accepted.');return false}if(f.size>5*1024*1024){error(cv,'Your file must be 5 MB or smaller.');return false}clearError(cv);return true}
 function showFile(){const f=cv.files?.[0];fileName.textContent=f?`✓ ${f.name} (${(f.size/1024/1024).toFixed(2)} MB)`:'';if(f)validateCV()}
 cv.addEventListener('change',showFile);
 ['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('dragging')}));
 ['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('dragging')}));
 drop.addEventListener('drop',e=>{if(e.dataTransfer?.files?.length){cv.files=e.dataTransfer.files;showFile()}});
 form.querySelectorAll('input,select').forEach(field=>field.addEventListener('input',()=>{clearError(field);msg.textContent='';msg.classList.remove('success');if(field.id==='consent' && field.checked)$('#consent-error').textContent=''}));
 function validLinkedin(s){try{const u=new URL(s);return u.protocol==='https:' && /^(www\.|[a-z]{2}\.)?linkedin\.com$/i.test(u.hostname) && /^\/(in|pub)\//i.test(u.pathname)}catch{return false}}
 function validate(){let ok=true;msg.textContent='';msg.classList.remove('success');
  for(const f of form.querySelectorAll('input[required],select[required]')){
   if(f.type==='file'||f.type==='checkbox')continue;
   f.value=f.value.trim();if(!f.value){error(f,'This field is required.');ok=false}
   else if(f.type==='email'&&!f.checkValidity()){error(f,'Enter a valid email address.');ok=false}
   else if(f.id==='mobile'&&!/^\+?[0-9() .-]{7,25}$/.test(f.value)){error(f,'Enter a valid mobile phone number.');ok=false}
   else if(f.id==='linkedin'&&!validLinkedin(f.value)){error(f,'Enter a full HTTPS LinkedIn profile URL.');ok=false}
   else if(f.id==='dob'&&f.value>isoToday){error(f,'Date of birth cannot be in the future.');ok=false}
   else if(f.id==='start_date'&&f.value<isoToday){error(f,'Choose today or a future start date.');ok=false}
  }
  if(applicant.value==='foreigner'&&!/^[\p{L}\p{N}\- ]{4,30}$/u.test(passport.value.trim())){error(passport,'Enter a valid passport number (4–30 characters).');ok=false}
  if(!validateCV())ok=false;
  const consent=$('#consent');$('#consent-error').textContent=consent.checked?'':'Please consent before submitting.';if(!consent.checked)ok=false;
  if(!ok){const first=form.querySelector('.invalid')||(consent.checked?null:consent);first?.focus();msg.textContent='Please check the highlighted fields and try again.'}
  return ok;
 }
 form.addEventListener('submit',async e=>{e.preventDefault();if(!validate())return;
  if(root.dataset.mode==='preview'){msg.textContent='Your details pass the preview checks. No application has been sent. Install and configure the WordPress plugin to enable secure delivery.';msg.classList.add('success');return}
  const config=window.amCareersConfig||{};
  if(!config.endpoint||!config.nonce){msg.textContent='The application service is not configured. Please contact the site administrator.';return}
  const data=new FormData(form);data.append('action','am_careers_submit');data.append('nonce',config.nonce);
  button.disabled=true;button.querySelector('span').textContent='SENDING...';
  try{const response=await fetch(config.endpoint,{method:'POST',body:data,credentials:'same-origin'});const body=await response.json();
   if(!response.ok||!body.success)throw new Error(body?.data?.message||'Your application could not be delivered. Please try again.');
   form.reset();fileName.textContent='';passportState();msg.textContent='Application sent successfully. Thank you for introducing yourself!';msg.classList.add('success');msg.scrollIntoView({block:'nearest',behavior:'smooth'});
  }catch(ex){msg.textContent=ex.message||'Submission failed. Please try again.';msg.classList.remove('success')}
  finally{button.disabled=false;button.querySelector('span').textContent='SUBMIT APPLICATION'}
 });
})();
