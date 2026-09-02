const LEGACY_WORDS_UNUSED = [
  {word:'相変わらず',kana:'あいかわらず',meaning:'변함없이, 여전히',type:'부사',example:'彼は相変わらず元気です。',translation:'그는 여전히 건강합니다.'},
  {word:'明らか',kana:'あきらか',meaning:'명백함, 분명함',type:'형용사',example:'それは明らかな間違いです。',translation:'그것은 명백한 실수입니다.'},
  {word:'諦める',kana:'あきらめる',meaning:'포기하다, 단념하다',type:'동사',example:'最後まで夢を諦めないでください。',translation:'끝까지 꿈을 포기하지 마세요.'},
  {word:'預ける',kana:'あずける',meaning:'맡기다',type:'동사',example:'駅のロッカーに荷物を預けました。',translation:'역 사물함에 짐을 맡겼습니다.'},
  {word:'扱う',kana:'あつかう',meaning:'다루다, 취급하다',type:'동사',example:'この店は外国の本も扱っています。',translation:'이 가게는 외국 책도 취급하고 있습니다.'},
  {word:'余る',kana:'あまる',meaning:'남다, 넘치다',type:'동사',example:'料理が少し余ってしまいました。',translation:'요리가 조금 남아 버렸습니다.'},
  {word:'意外',kana:'いがい',meaning:'의외',type:'명사',example:'試験は意外に簡単でした。',translation:'시험은 의외로 간단했습니다.'},
  {word:'維持',kana:'いじ',meaning:'유지',type:'명사',example:'健康を維持するために運動します。',translation:'건강을 유지하기 위해 운동합니다.'},
  {word:'一応',kana:'いちおう',meaning:'일단, 대강',type:'부사',example:'一応、予定を確認しておきます。',translation:'일단 일정을 확인해 두겠습니다.'},
  {word:'受け取る',kana:'うけとる',meaning:'받다, 수령하다',type:'동사',example:'受付で資料を受け取ってください。',translation:'접수처에서 자료를 받아 주세요.'},
  {word:'追いつく',kana:'おいつく',meaning:'따라잡다',type:'동사',example:'走って前の人に追いつきました。',translation:'달려서 앞사람을 따라잡았습니다.'},
  {word:'応じる',kana:'おうじる',meaning:'응하다, 대응하다',type:'동사',example:'お客様の希望に応じて変更します。',translation:'손님의 희망에 따라 변경합니다.'},
  {word:'おそらく',kana:'おそらく',meaning:'아마, 어쩌면',type:'부사',example:'明日はおそらく雨でしょう。',translation:'내일은 아마 비가 올 것입니다.'},
  {word:'解決',kana:'かいけつ',meaning:'해결',type:'명사',example:'みんなで問題を解決しました。',translation:'모두 함께 문제를 해결했습니다.'},
  {word:'確認',kana:'かくにん',meaning:'확인',type:'명사',example:'出発時間をもう一度確認します。',translation:'출발 시간을 다시 한번 확인합니다.'},
  {word:'限る',kana:'かぎる',meaning:'한정하다, 제한하다',type:'동사',example:'参加者は学生に限ります。',translation:'참가자는 학생으로 한정합니다.'},
  {word:'活発',kana:'かっぱつ',meaning:'활발함',type:'형용사',example:'彼女は活発で明るい人です。',translation:'그녀는 활발하고 밝은 사람입니다.'},
  {word:'感心',kana:'かんしん',meaning:'감탄, 탄복',type:'명사',example:'彼の努力には感心しました。',translation:'그의 노력에는 감탄했습니다.'},
  {word:'気づく',kana:'きづく',meaning:'깨닫다, 알아차리다',type:'동사',example:'駅に着いて忘れ物に気づきました。',translation:'역에 도착해서 두고 온 물건을 알아차렸습니다.'},
  {word:'具体的',kana:'ぐたいてき',meaning:'구체적',type:'형용사',example:'具体的な例を説明してください。',translation:'구체적인 예를 설명해 주세요.'},
  {word:'工夫',kana:'くふう',meaning:'궁리, 고안',type:'명사',example:'収納の仕方をいろいろ工夫しました。',translation:'수납 방법을 여러 가지로 궁리했습니다.'},
  {word:'加える',kana:'くわえる',meaning:'더하다, 추가하다',type:'동사',example:'スープに少し塩を加えます。',translation:'수프에 소금을 조금 더합니다.'},
  {word:'傾向',kana:'けいこう',meaning:'경향',type:'명사',example:'最近は物価が上がる傾向にあります。',translation:'최근에는 물가가 오르는 경향이 있습니다.'},
  {word:'決して',kana:'けっして',meaning:'결코, 절대로',type:'부사',example:'私は決して約束を忘れません。',translation:'저는 결코 약속을 잊지 않습니다.'},
  {word:'断る',kana:'ことわる',meaning:'거절하다, 사양하다',type:'동사',example:'忙しかったので誘いを断りました。',translation:'바빴기 때문에 권유를 거절했습니다.'},
  {word:'支える',kana:'ささえる',meaning:'지탱하다, 지원하다',type:'동사',example:'家族がいつも私を支えてくれます。',translation:'가족이 언제나 저를 지지해 줍니다.'},
  {word:'次第',kana:'しだい',meaning:'하는 대로, 여하',type:'명사',example:'準備ができ次第、出発します。',translation:'준비가 되는 대로 출발합니다.'},
  {word:'徐々に',kana:'じょじょに',meaning:'서서히, 조금씩',type:'부사',example:'天気は徐々に回復しています。',translation:'날씨는 서서히 회복되고 있습니다.'},
  {word:'優れる',kana:'すぐれる',meaning:'뛰어나다',type:'동사',example:'この製品は安全性に優れています。',translation:'이 제품은 안전성이 뛰어납니다.'},
  {word:'積極的',kana:'せっきょくてき',meaning:'적극적',type:'형용사',example:'会議で積極的に意見を言いました。',translation:'회의에서 적극적으로 의견을 말했습니다.'},
  {word:'尊敬',kana:'そんけい',meaning:'존경',type:'명사',example:'私は祖父を心から尊敬しています。',translation:'저는 할아버지를 진심으로 존경합니다.'},
  {word:'確かめる',kana:'たしかめる',meaning:'확인하다, 확실히 하다',type:'동사',example:'住所が正しいか確かめてください。',translation:'주소가 맞는지 확인해 주세요.'},
  {word:'偶然',kana:'ぐうぜん',meaning:'우연',type:'명사',example:'駅で友達に偶然会いました。',translation:'역에서 친구를 우연히 만났습니다.'},
  {word:'不足',kana:'ふそく',meaning:'부족',type:'명사',example:'この町では医師が不足しています。',translation:'이 마을에서는 의사가 부족합니다.'},
  {word:'ますます',kana:'ますます',meaning:'더욱더, 점점 더',type:'부사',example:'日本語の勉強がますます楽しくなりました。',translation:'일본어 공부가 점점 더 즐거워졌습니다.'},
  {word:'認める',kana:'みとめる',meaning:'인정하다, 허가하다',type:'동사',example:'彼は自分の失敗を認めました。',translation:'그는 자신의 실패를 인정했습니다.'}
];

const VOCABULARY_CORRECTIONS={
  'うがい':{meaning:'가글, 입 헹구기',translation:'가글했어?'},
  '夜':{kana:'よる',example:'夜は静かです。',translation:'밤은 조용합니다.'},
  '今日':{kana:'きょう',meaning:'오늘',type:'명사·부사',example:'今日も頑張りましょう。',translation:'오늘도 힘냅시다.'},
  'すてき':{meaning:'멋진, 근사한',type:'형용사',example:'すてきな服ですね。',translation:'멋진 옷이네요.'},
  '演奏':{meaning:'연주',type:'명사',example:'彼女はピアノを演奏する。',translation:'그녀는 피아노를 연주한다.'},
  'いち':{word:'市',meaning:'장터, 시장',type:'명사',example:'毎月ここで市が開かれる。',translation:'매달 이곳에서 장이 열린다.'},
  '身':{meaning:'몸, 신체, 자신',type:'명사',example:'自分の身を守ってください。',translation:'자신의 몸을 지켜 주세요.'},
  '世間':{meaning:'세상, 사회, 세간',type:'명사',example:'世間の目を気にする。',translation:'세상의 시선을 신경 쓴다.'},
  '弁当':{meaning:'도시락',type:'명사',example:'駅で弁当を買った。',translation:'역에서 도시락을 샀다.'},
  '日常':{meaning:'일상, 평소',type:'명사',example:'運動を日常に取り入れる。',translation:'운동을 일상에 들인다.'},
  '友':{meaning:'친구, 벗',type:'명사',example:'彼は長年の友です。',translation:'그는 오랜 친구입니다.'},
  '怠ける':{meaning:'게으름 피우다, 태만하다',type:'동사',example:'仕事を怠けてはいけない。',translation:'일을 게으름 피우면 안 된다.'},
  'お腹':{meaning:'배, 뱃속',type:'명사',example:'お腹が痛いの？',translation:'배가 아파?'},
  'あっ':{meaning:'아!, 어!',type:'감탄사',example:'あっ、財布を忘れた。',translation:'아, 지갑을 깜빡했다.'}
};
const VERB_MEANING_CORRECTIONS={
  '愛する':'사랑하다','明ける':'밝아지다, 끝나다','浴びる':'뒤집어쓰다, 샤워하다','現す':'나타내다','現れる':'나타나다','頂く':'받다, 먹다·마시다의 겸양어','至る':'이르다, 도달하다','撃つ':'쏘다, 공격하다','移す':'옮기다','奪う':'빼앗다','裏切る':'배신하다','売れる':'팔리다','終える':'끝내다','贈る':'선물하다, 보내다','収める':'거두다, 납부하다','溺れる':'물에 빠지다','降ろす':'내리다','飼う':'기르다','換える':'바꾸다, 교환하다','替える':'바꾸다, 교체하다','隠す':'숨기다','隠れる':'숨다','欠ける':'부족하다, 깨지다','稼ぐ':'벌다','数える':'세다','被る':'뒤집어쓰다, 입다','構う':'상관하다, 신경 쓰다','関する':'관계하다','効く':'효과가 있다','暮らす':'살다, 생활하다','狂う':'미치다, 어긋나다','殺す':'죽이다','誘う':'권유하다, 유혹하다','覚ます':'깨우다','覚める':'깨다','支払う':'지불하다','示す':'나타내다, 보여 주다','占める':'차지하다','空く':'비다','救う':'구하다, 구해 내다','済ませる':'끝내다, 처리하다','責める':'비난하다, 책망하다','備える':'갖추다, 대비하다','対する':'대하다','戦う':'싸우다','立ち上がる':'일어서다','達する':'도달하다','通じる':'통하다, 이해되다','掴む':'붙잡다','付ける':'붙이다, 더하다','繋ぐ':'잇다, 연결하다','詰める':'채우다, 줄이다','出会う':'우연히 만나다','解く':'풀다','届く':'도착하다, 닿다','飛ばす':'날리다, 건너뛰다','飛び出す':'뛰쳐나오다','留める':'고정하다, 붙잡아 두다','取り上げる':'집어 들다, 빼앗다','流す':'흘리다','握る':'쥐다','濡れる':'젖다','除く':'제외하다, 제거하다','伸びる':'늘어나다, 성장하다','述べる':'서술하다, 말하다','昇る':'오르다','計る':'재다, 계산하다','外す':'빼다, 벗기다','放す':'놓다, 풀어 주다','離す':'떼어 놓다','省く':'생략하다, 줄이다','張る':'치다, 붙이다','引っ張る':'잡아당기다','打つ':'치다','微笑む':'미소 짓다','招く':'초대하다, 불러오다','守る':'지키다','回す':'돌리다','満ちる':'가득 차다','向く':'향하다','命じる':'명령하다, 임명하다','燃える':'타다','用いる':'사용하다','戻す':'되돌리다','辞める':'그만두다','言う':'말하다','譲る':'양보하다, 넘겨주다','許す':'허락하다, 용서하다','分ける':'나누다, 구분하다'
};
WORDS.forEach(word=>{const originalWord=word.word;const correction=VOCABULARY_CORRECTIONS[originalWord];if(correction)Object.assign(word,correction);if(VERB_MEANING_CORRECTIONS[originalWord])word.meaning=VERB_MEANING_CORRECTIONS[originalWord]});
Object.assign(WORDS.find(word=>word.word==='あんなに')||{},{meaning:'저렇게, 그렇게',type:'부사'});
Object.assign(WORDS.find(word=>word.word==='先ず')||{},{meaning:'먼저, 우선',type:'부사'});
const POS_CORRECTIONS={
  '頂く':{meaning:'받다, 먹다, 마시다',type:'동사'},'集まり':{meaning:'모임, 집합',type:'명사'},'ありがとう':{meaning:'고마움, 감사',type:'표현'},'おしゃべり':{meaning:'수다, 수다쟁이',type:'명사'},'穏やか':{meaning:'온화하다, 평온하다',type:'형용사'},'がっかり':{meaning:'실망하다, 낙담하다',type:'부사·표현'},'食う':{meaning:'먹다',type:'동사'},'濃い':{meaning:'짙다, 진하다',type:'형용사'},'鋭い':{meaning:'날카롭다, 예리하다',type:'형용사'},'違いない':{meaning:'틀림없다',type:'표현'},'どれ':{meaning:'어느 것',type:'대명사'},'訳':{meaning:'의미, 이유, 사정',type:'명사'},'ハンサム':{meaning:'잘생기다, 멋지다',type:'형용사'},'そっくり':{meaning:'똑같이, 꼭 닮게',type:'부사'},'まさに':{meaning:'바로, 틀림없이',type:'부사'}
};
WORDS.forEach(word=>{if(POS_CORRECTIONS[word.word])Object.assign(word,POS_CORRECTIONS[word.word])});

const STORAGE_KEY='kimheekyo-n3-progress-v2';
let state=loadState(); let quiz=[]; let quizIndex=0; let quizScore=0; let direction='jp-ko'; let quizMode='daily'; let quizRoundOffset=0;
function loadState(){try{return {...{answered:0,correct:0,mastered:[],wrong:[],date:todayKey()},...JSON.parse(localStorage.getItem(STORAGE_KEY)||'{}')}}catch{return {answered:0,correct:0,mastered:[],wrong:[],date:todayKey()}}}
function todayKey(){return new Date().toISOString().slice(0,10)}
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state));updateStats()}
function shuffle(a){return [...a].sort(()=>Math.random()-.5)}
function escapeHtml(s){return s.replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
function quizMeaning(w){return w.meaning.split(',')[0].trim()}
function wordWithReading(w){return `<span class="written">${escapeHtml(w.word)}</span>`}
function exampleWithReading(w){const sentence=escapeHtml(w.example);if(!w.kana||w.kana===w.word)return sentence;const target=escapeHtml(w.word);const index=sentence.indexOf(target);if(index<0)return sentence;const before=sentence[index-1]||'';const after=sentence[index+target.length]||'';const kanji=/[\u3400-\u9fff々]/;if((before&&kanji.test(before))||(after&&kanji.test(after)))return sentence;return sentence.replace(target,`<ruby>${target}<rt>${escapeHtml(w.kana)}</rt></ruby>`)}
function pickDistractors(w,jp){const correctMeaning=quizMeaning(w);const seen=new Set([jp?correctMeaning:w.word]);return shuffle(WORDS).filter(x=>{if(x===w||(!jp&&quizMeaning(x)===correctMeaning))return false;const displayed=jp?quizMeaning(x):x.word;if(seen.has(displayed))return false;seen.add(displayed);return true}).slice(0,3)}
function setQuizAwaiting(active){document.documentElement.classList.toggle('quiz-awaiting-answer',active);document.body.classList.toggle('quiz-awaiting-answer',active)}
function setQuizIntroLayout(active){document.documentElement.classList.toggle('quiz-intro-active',active);document.body.classList.toggle('quiz-intro-active',active)}
function showView(id){setQuizAwaiting(false);setQuizIntroLayout(id==='quiz'&&!document.querySelector('#quizIntro').classList.contains('hidden'));const home=id==='home';document.documentElement.classList.toggle('home-active',home);document.body.classList.toggle('home-active',home);document.querySelectorAll('.view').forEach(v=>v.classList.toggle('active',v.id===id));document.querySelectorAll('.nav-button').forEach(b=>b.classList.toggle('active',b.dataset.view===id));if(id==='words')renderWords();if(id==='review')renderReview();scrollTo({top:0,behavior:'smooth'})}
document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view)));
function openQuizIntro(mode){if(mode)setQuizMode(mode);document.querySelector('#quizGame').classList.add('hidden');document.querySelector('#quizResult').classList.add('hidden');document.querySelector('#quizIntro').classList.remove('hidden');setQuizIntroLayout(true)}
document.addEventListener('click',e=>{const b=e.target.closest('[data-go]');if(!b)return;e.preventDefault();if(b.dataset.go==='quiz')openQuizIntro(b.dataset.quizMode);showView(b.dataset.go)});
function setQuizMode(mode){quizMode=mode;const endless=mode==='random';document.querySelector('#quizIntroLabel').textContent=endless?'ENDLESS QUIZ':'10 QUESTIONS';document.querySelector('#quizIntroTitle').textContent=endless?'무제한 랜덤 퀴즈':'오늘의 퀴즈';document.querySelector('#quizIntroCopy').innerHTML=endless?'전체 단어에서 문제가 계속 출제됩니다.<br>그만하고 싶을 때 나가기를 누르세요.':'뜻을 맞히면 예문이 공개됩니다.<br>틀린 단어는 오답노트에 자동으로 담겨요.'}
function updateStats(){if(state.date!==todayKey()){state.answered=0;state.correct=0;state.date=todayKey();save();return}document.querySelector('#answeredStat').textContent=state.answered;document.querySelector('#accuracyStat').textContent=state.answered?Math.round(state.correct/state.answered*100)+'%':'—';document.querySelector('#accuracyCaption').textContent=state.answered?`${state.correct}개 정답`:'첫 문제를 풀어보세요';document.querySelector('#masteredStat').textContent=state.mastered.length;document.querySelector('#reviewCount').textContent=state.wrong.length;document.querySelector('#wordTotal').textContent=`N3 핵심 ${WORDS.length}단어`}
function cardHtml(w){return `<article class="word-card" tabindex="0"><span class="tag">${w.type}</span><h3>${w.word}</h3><span class="kana">${w.kana}</span><p class="meaning">${w.meaning}</p><div class="card-example"><p>${w.example}</p><small>${w.translation}</small></div></article>`}
function bindCards(root){root.querySelectorAll('.word-card').forEach(c=>{const toggle=()=>c.classList.toggle('open');c.addEventListener('click',toggle);c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle()}})})}
function renderWords(){const q=document.querySelector('#wordSearch').value.trim().toLowerCase();const type=document.querySelector('#categoryFilter').value;const list=WORDS.filter(w=>(type==='all'||w.type===type)&&[w.word,w.kana,w.meaning].some(x=>x.toLowerCase().includes(q)));const grid=document.querySelector('#wordGrid');grid.innerHTML=list.map(cardHtml).join('');document.querySelector('#emptyWords').classList.toggle('hidden',list.length>0);bindCards(grid)}
document.querySelector('#wordSearch').addEventListener('input',renderWords);document.querySelector('#categoryFilter').addEventListener('change',renderWords);
function renderReview(){const list=state.wrong.map(i=>WORDS[i]).filter(Boolean);const grid=document.querySelector('#reviewGrid');grid.innerHTML=list.map(cardHtml).join('');document.querySelector('#emptyReview').classList.toggle('hidden',list.length>0);bindCards(grid)}
function startQuiz(){setQuizIntroLayout(false);direction=document.querySelector('input[name="direction"]:checked').value;quiz=shuffle(WORDS.map((_,i)=>i));if(quizMode==='daily')quiz=quiz.slice(0,10);quizIndex=0;quizScore=0;quizRoundOffset=0;document.querySelector('#quizIntro').classList.add('hidden');document.querySelector('#quizResult').classList.add('hidden');document.querySelector('#quizGame').classList.remove('hidden');document.querySelector('#progressTrack').classList.toggle('hidden',quizMode==='random');renderQuestion()}
function renderQuestion(){setQuizAwaiting(true);const w=WORDS[quiz[quizIndex]];const jp=direction==='jp-ko';const reading=document.querySelector('#questionReading');const hint=document.querySelector('#readingHint');const canHint=jp&&w.kana!==w.word;document.querySelector('#quizProgress').textContent=quizMode==='random'?`${quizRoundOffset+quizIndex+1}번째 문제`:`${quizIndex+1} / ${quiz.length}`;document.querySelector('#quizScore').textContent=`정답 ${quizScore}`;document.querySelector('#progressBar').style.width=`${(quizIndex+1)/quiz.length*100}%`;document.querySelector('#questionLabel').textContent=jp?'다음 단어의 뜻은?':'다음 뜻에 맞는 일본어는?';document.querySelector('#questionText').textContent=jp?w.word:quizMeaning(w);reading.textContent=canHint?w.kana:'';reading.classList.add('hidden');hint.classList.toggle('hidden',!canHint);document.querySelector('#answerPanel').classList.add('hidden');const distractors=pickDistractors(w,jp);const opts=shuffle([w,...distractors]);const box=document.querySelector('#options');box.innerHTML=opts.map(x=>`<button class="option" data-correct="${x===w}">${jp?escapeHtml(quizMeaning(x)):wordWithReading(x)}</button>`).join('');box.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>answer(b,w)))}
function answer(button,w){setQuizAwaiting(false);document.querySelector('#readingHint').classList.add('hidden');document.querySelector('#questionReading').classList.remove('hidden');const correct=button.dataset.correct==='true';document.querySelectorAll('.option').forEach(b=>{b.disabled=true;if(b.dataset.correct==='true')b.classList.add('correct')});if(!correct)button.classList.add('wrong');if(correct){quizScore++;state.correct++;if(!state.mastered.includes(quiz[quizIndex]))state.mastered.push(quiz[quizIndex]);state.wrong=state.wrong.filter(i=>i!==quiz[quizIndex])}else if(!state.wrong.includes(quiz[quizIndex]))state.wrong.push(quiz[quizIndex]);state.answered++;save();document.querySelector('#answerResult').textContent=correct?'정답이에요! ✓':`아쉬워요. 정답은 ‘${direction==='jp-ko'?quizMeaning(w):w.word}’`;document.querySelector('#answerResult').style.color=correct?'#347050':'#bd5545';document.querySelector('#answerReading').textContent=w.kana!==w.word?`${w.word}（${w.kana}）`:w.word;document.querySelector('#exampleJp').innerHTML=exampleWithReading(w);document.querySelector('#exampleKo').textContent=w.translation;document.querySelector('#nextQuestion').textContent=quizIndex===quiz.length-1&&quizMode==='daily'?'결과 보기 →':'다음 문제 →';document.querySelector('#answerPanel').classList.remove('hidden')}
function nextQuestion(){quizIndex++;if(quizIndex<quiz.length){renderQuestion();return}if(quizMode==='random'){quizRoundOffset+=quiz.length;quiz=shuffle(WORDS.map((_,i)=>i));quizIndex=0;renderQuestion();return}document.querySelector('#quizGame').classList.add('hidden');document.querySelector('#quizResult').classList.remove('hidden');document.querySelector('#resultCopy').textContent=`10문제 중 ${quizScore}문제를 맞혔어요. ${quizScore>=8?'훌륭해요! 이 흐름을 이어가세요.':quizScore>=5?'좋아요! 헷갈린 단어를 한 번 더 볼까요?':'오답노트로 차근차근 익혀봐요.'}`}
document.querySelector('#startQuiz').addEventListener('click',startQuiz);document.querySelector('#retryQuiz').addEventListener('click',startQuiz);document.querySelector('#nextQuestion').addEventListener('click',nextQuestion);document.querySelector('#readingHint').addEventListener('click',()=>{document.querySelector('#readingHint').classList.add('hidden');document.querySelector('#questionReading').classList.remove('hidden')});document.querySelector('#quitQuiz').addEventListener('click',()=>{setQuizAwaiting(false);setQuizIntroLayout(true);document.querySelector('#quizGame').classList.add('hidden');document.querySelector('#quizIntro').classList.remove('hidden')});
document.querySelector('#todayDate').textContent=new Intl.DateTimeFormat('ko-KR',{month:'long',day:'numeric',weekday:'short'}).format(new Date());updateStats();renderReview();

function showUpdateNotice(registration){
  const notice=document.querySelector('#updateNotice');
  const apply=document.querySelector('#applyUpdate');
  const dismiss=document.querySelector('#dismissUpdate');
  if(!notice||!registration.waiting)return;
  notice.classList.remove('hidden');
  apply.onclick=()=>{apply.disabled=true;apply.textContent='업데이트 중…';registration.waiting?.postMessage({type:'SKIP_WAITING'})};
  dismiss.onclick=()=>notice.classList.add('hidden');
}

if('serviceWorker' in navigator&&location.protocol!=='file:'){
  let refreshing=false;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{if(refreshing)return;refreshing=true;location.reload()});
  window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').then(registration=>{
    if(registration.waiting)showUpdateNotice(registration);
    registration.addEventListener('updatefound',()=>{
      const worker=registration.installing;
      worker?.addEventListener('statechange',()=>{
        if(worker.state==='installed'&&navigator.serviceWorker.controller)showUpdateNotice(registration);
      });
    });
    setInterval(()=>registration.update(),60*60*1000);
  }).catch(error=>console.warn('오프라인 앱을 준비하지 못했습니다.',error)));
}
