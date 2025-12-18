import json
import time
import requests
from wordfreq import word_frequency
from collections import Counter

# SAT 고난도 단어 2000개 리스트
sat_words_raw = """
aberration,abstruse,accolade,acrimony,admonish,aesthetic,affable,alacrity,alleviate,amalgamate,
ambivalent,ameliorate,anachronism,analogous,anathema,anomaly,antithesis,apathy,appease,arbitrary,
arcane,arduous,articulate,ascetic,assiduous,astute,atrophy,audacious,augment,auspicious,
austere,avarice,banal,belie,bellicose,belligerent,benevolent,berate,bolster,bombastic,
boorish,burgeon,cacophony,cajole,callous,candor,capricious,caustic,censure,chicanery,
circumspect,clandestine,clemency,coalesce,cogent,commensurate,compelling,complacent,compliant,conciliatory,
condone,conflagration,congenial,conjecture,connive,connoisseur,consecrate,contentious,contrite,
conundrum,converge,convoluted,copious,corroborate,credulous,cryptic,culpable,cursory,curtail,
cynical,daunt,dearth,debunk,decorum,defamation,deference,deft,deleterious,delineate,
demagogue,demure,denigrate,denounce,deplete,deride,derivative,desiccate,despondent,despot,
deter,detract,devious,diatribe,dichotomy,didactic,diffident,digress,dilatory,diligent,
diminish,discern,discreet,discrepancy,disdain,disparage,disparate,disseminate,dissident,dissolution,
dissonance,diverge,docile,dogmatic,dormant,dubious,duplicity,ebullient,eccentric,eclectic,
efficacy,effrontery,egregious,elated,elicit,eloquent,elucidate,elusive,embellish,emulate,
endemic,enervate,engender,enigma,enmity,enumerate,ephemeral,equanimity,equivocal,eradicate,
erratic,erudite,esoteric,espouse,ethereal,euphemism,exacerbate,exalt,exasperate,exemplary,
exhaustive,exonerate,expedient,explicit,exploit,expunge,extol,extraneous,extricate,exuberant,
facetious,facilitate,fallacious,fastidious,fatuous,fawn,feasible,fervent,fickle,flagrant,
florid,flourish,foment,forestall,fortuitous,foster,fractious,frivolous,frugal,furtive,
futile,galvanize,garrulous,germane,grandiloquent,gratuitous,gregarious,guile,hackneyed,hamper,
haphazard,harbinger,hardy,hasten,haughty,hedonism,heresy,hierarchy,homogeneous,hubris,
hyperbole,hypothetical,iconoclast,idiosyncrasy,ignominious,illicit,immutable,impartial,impeccable,impede,
impending,imperious,impervious,impetuous,implicit,impudent,inadvertent,incendiary,incipient,incisive,
incongruous,inconsequential,incontrovertible,incorrigible,incredulous,indefatigable,indigenous,indignant,indolent,indomitable,
ineffable,inept,inexorable,infamous,ingenious,ingenuous,inherent,innate,innocuous,innovative,
insatiable,insidious,insinuate,insipid,insolent,instigate,insurgent,integral,integrity,intrepid,
intricate,intrinsic,inundate,invective,invoke,irascible,irresolute,irreverent,itinerant,jocular,
judicious,juxtapose,kindle,labyrinth,laconic,languid,laud,lethargic,levity,litigate,
loquacious,lucid,ludicrous,magnanimous,malevolent,malign,malleable,mandate,manifest,mar,
meander,meticulous,mitigate,mollify,morose,mundane,munificent,myriad,nascent,nefarious,
negligent,neophyte,nonchalant,notorious,novel,nuance,obdurate,objective,oblivious,obscure,
obsequious,obstinate,obtuse,obviate,ominous,onerous,opaque,opportunist,optimum,orthodox,
oscillate,ostentatious,overt,palatable,panacea,paradigm,paradox,paragon,paramount,pariah,
parody,parsimonious,partisan,pathological,patronize,paucity,pedantic,penchant,penitent,perceptive,
perfidious,perfunctory,peripheral,perjury,permeate,pernicious,perpetuate,perplexing,perseverance,pertinent,
pervasive,petulant,philanthropic,phlegmatic,piety,pinnacle,placate,platitude,plausible,plethora,
poignant,polarize,polemical,ponderous,pragmatic,precarious,precedent,precipitate,preclude,precocious,
predecessor,predilection,preeminent,premise,prerogative,prescient,presumptuous,pretentious,prevalent,pristine,
probity,proclivity,procrastinate,prodigal,prodigious,profane,proficient,profound,profuse,proliferate,
prolific,propensity,prophetic,propitious,propriety,prosaic,proscribe,prosperity,protagonist,provincial,
provocative,prudent,pugnacious,punctilious,pungent,punitive,quandary,querulous,quintessential,rancor,
ratify,raucous,ravenous,rebuke,recalcitrant,recant,receptive,reclusive,reconcile,rectify,
redundant,refute,relegate,relentless,relinquish,remedial,remorse,renounce,replete,reprehensible,
repress,reprimand,repudiate,requisite,rescind,resilient,resolute,resonate,restitution,restive,
reticent,retract,reverent,rhetoric,rigorous,robust,rudimentary,ruminate,rustic,sacrosanct,
sagacious,salient,sanction,sanguine,satirical,saturate,scathing,scrupulous,scrutinize,sedentary,
seditious,serendipity,serene,servile,shrewd,singular,skeptical,slander,solace,
solicit,solvent,somber,soporific,sparse,specious,sporadic,spurious,squalid,squander,
stagnant,staunch,steadfast,stoic,stratagem,strident,stringent,subordinate,subpoena,substantiate,
subtle,subversive,succinct,superficial,superfluous,supplant,suppress,surmise,surreptitious,susceptible,
sustain,sycophant,synthesis,tacit,tangential,tangible,tedious,temerity,temperament,temperate,
tenacious,tentative,tenuous,terse,tirade,torpid,torrent,tortuous,tractable,tranquil,
transcend,transient,transparent,trepidation,trite,trivial,truculent,turbulent,turmoil,ubiquitous,
unanimity,undermine,underscore,unequivocal,unfounded,unprecedented,unscrupulous,untenable,unwitting,upbraid,
usurp,utilitarian,vacillate,vehement,venerate,veracity,verbose,vestige,viable,vicarious,
vigilant,vilify,vindicate,vindictive,virtuoso,virulent,visceral,vitriolic,vivacious,volatile,
voracious,vulnerable,wane,wary,whimsical,wistful,zealot,zenith,
abate,abjure,abnegate,abrogate,absolve,abstain,abstemious,abstinent,abysmal,accede,
accentuate,accost,accrue,acquiesce,acrid,acumen,adamant,adroit,adulation,adversary,
advocate,affinity,affluent,aggrandize,aggregate,aggrieve,altruism,amenable,amicable,
amorphous,amplify,anarchist,anecdote,animosity,annex,annihilate,annotate,antagonize,antecedent,
antipathy,antiquated,aphorism,aplomb,apocalyptic,apocryphal,apotheosis,apprehensive,approbation,
arbiter,archaism,ardent,arid,arrogate,artifice,
ascribe,asperity,aspersion,assail,assent,assuage,atone,audacity,augury,
autocrat,autonomous,auxiliary,aversion,avid,avocation,baleful,balk,
banality,bane,bastion,beatific,bedlam,begrudge,beguile,behemoth,bemoan,benefactor,
benign,bequeath,beseech,besiege,bestow,biased,bifurcate,blasphemy,
blatant,blemish,blight,blithe,boisterous,brash,brazen,brevity,bristle,
broach,bromide,bucolic,bureaucracy,burlesque,buttress,cabal,cadence,caliber,calumny,
canon,canvass,capacious,capitulate,caricature,cascade,castigate,
catalyst,categorical,caucus,cavalier,cavil,cede,cerebral,chagrin,charlatan,
chasm,chastise,chronicle,circuitous,circumlocution,circumscribe,circumvent,
clairvoyant,clamor,cleave,coax,coerce,cogitate,
cohesion,collaborate,collateral,colloquial,collusion,commodious,commiserate,compatible,compel,
compensate,comport,comprise,compunction,concede,conception,concerted,concoct,
concomitant,concurrent,condescend,confiscate,confluence,conformity,confound,congeal,
congenital,conglomerate,congruent,connote,conscientious,constrain,construe,consummate,contemn,
contemplative,contempt,contend,contingent,contraband,contravene,contrition,controvert,convene,
convivial,cordial,corollary,corporeal,correlate,countenance,counterfeit,
covenant,covert,covet,crass,craven,credence,creed,criterion,critique,cull,
culminate,culprit,cumbersome,cupidity,curmudgeon,daunting,debacle,debase,debilitate,
decadence,decimate,decipher,decree,decry,deface,defection,
defer,defile,definitive,deflect,defunct,degrade,deign,delectable,deliberate,
deluge,delusion,demean,demeanor,demolish,denizen,denote,
depict,deplore,deploy,depose,deprecate,derelict,derogatory,desecrate,
desolate,despicable,despoil,destitute,detain,devoid,devout,dexterous,
dialectic,dictum,diffuse,dilettante,dilapidated,dilate,diminution,dire,
dirge,disabuse,disarray,disavow,discernible,disclose,discord,
discourse,disenfranchise,disgruntle,dishearten,disheveled,disingenuous,disinterested,
dislodge,dismal,dismantle,dispatch,dispel,disperse,displace,
disquiet,disrepute,dissect,dissemble,dissent,dissipate,dissolute,
distend,distill,distort,distraught,diverse,divest,divulge,
dogged,doldrums,dolorous,dolt,domineer,dotage,doughty,
dour,draconian,droll,drone,drudgery,dubiety,dulcet,
dupe,duress,dwindle,earnest,ebb,ebullience,eclipse,edifice,efface,
effervescent,effete,effigy,effusive,egalitarian,elaborate,elegy,elevated,
elliptical,emaciate,emanate,emancipate,embargo,embark,embody,
embroil,eminent,empathy,empirical,encapsulate,
enclave,encompass,encroach,encumber,endorse,endow,enfranchise,
engross,enhance,enjoin,enmesh,enrapture,ensconce,ensue,entail,
enthrall,entice,entourage,entreat,entrench,enunciate,envision,
epitome,epoch,equitable,erode,erstwhile,escalate,eschew,
esteem,estrange,eulogy,euphoria,evanescent,evasive,
evict,evince,evoke,exacting,excavate,exceed,excerpt,
excise,exclude,excoriate,exculpate,execrate,exemplify,exempt,exert,
exhibit,exhilarate,exhort,exigent,exile,exorbitant,expansive,expatriate,
expectorate,expedite,expel,expiate,explicate,exponent,
expound,expropriate,exquisite,extant,extemporaneous,extenuate,
exterminate,extinguish,extradite,extrinsic,exude,
fabricate,facade,facile,faction,fallacy,falter,fanatical,
farce,fathom,fatigue,faze,fealty,feckless,
fecund,feign,felicitous,feral,ferocious,ferret,fester,
fetid,fetter,feud,fiasco,fidelity,figment,filch,filibuster,
finesse,finite,fitful,flair,flamboyant,flaunt,fledgling,fleece,
flighty,flinch,flippant,flounder,fluctuate,fluke,
flux,foible,foil,foolhardy,forbearance,foreshadow,forfeit,forge,
formidable,forsake,forte,forthright,fortify,founder,fracas,
frail,frenetic,frenzy,frigid,fruition,frustrate,fugitive,fulminate,fulsome,
furor,futility,gadfly,gaffe,gait,gall,gambit,
garble,garish,garner,garnish,gauche,gaunt,generic,genesis,
genial,genre,genteel,germinal,gestation,gesticulate,ghastly,
gibe,gild,gingerly,gist,glacial,glean,glib,
gloat,glower,glut,goad,gorge,gossamer,gouge,
grandeur,graphic,grapple,gratify,grave,
grievance,grievous,grimace,grisly,
grotesque,grovel,grudge,grueling,gruff,guffaw,
haggard,haggle,hallmark,hallow,hallucination,halting,hankering,harass,
harmonious,harrowing,harsh,haven,havoc,
headstrong,heave,heckle,hectic,hedge,hegemony,heinous,
herald,heretic,heritage,hermetic,heterodox,heyday,hiatus,hidebound,
hideous,hinder,histrionic,hoard,hoax,hodgepodge,holocaust,homage,
homily,hone,hoodwink,hortatory,hospitable,hostile,hovel,
hover,hubbub,hue,humane,humdrum,humility,hurtle,
hybrid,hypocrite,hysteria,
iconoclastic,immaculate,immerse,imminent,impassive,impeach,impeccant,impecunious,
imperative,imperceptible,impermeable,impertinent,imperturbable,impervious,impetus,impious,
implacable,implausible,implicate,implore,impolitic,importune,imposing,impotent,
imprecation,impregnable,impromptu,improvident,impugn,impunity,inarticulate,incantation,
incarcerate,incarnate,incense,inception,incessant,inchoate,incidence,incinerate,
inclement,incline,incoherent,incommodious,incompatible,inconceivable,inconclusive,inconsequent,
inconsistent,incontinent,incorporate,incorruptible,increment,incriminate,incubate,inculcate,
incumbent,incur,indebted,indelible,indemnify,indent,indeterminate,indicative,
indices,indict,indifferent,indigence,indiscernible,indiscriminate,indispensable,indisposed,
indisputable,indistinct,indoctrinate,indomitable,indubitable,induce,indulge,industrious,
inebriated,inedible,inefficacious,ineluctable,inept,inequity,inert,inestimable,
inevitable,inexact,inexcusable,inexhaustible,inexpedient,inextricable,infallible,infantile,
infatuated,infer,infernal,infest,infiltrate,infinitesimal,infirm,inflame,
inflate,inflexible,inflict,influential,infraction,infringe,infuriate,infuse,
ingenuous,inglorious,ingrained,ingrate,ingratiate,inhabit,inherent,inhibit,
inimical,inimitable,iniquity,initiate,injunction,inklings,innuendo,inopportune,
inordinate,inquest,inquisitive,inscrutable,insensate,insentient,inseparable,insinuate,
insolence,insomnia,inspid,instantaneous,instigate,instill,institute,instrument,
insubordinate,insufferable,insular,insuperable,insurgence,insurmountable,insurrection,intangible,
integrate,intelligible,intemperance,intensify,intent,inter,intercede,interdict,
interim,interject,interloper,interminable,intermittent,internecine,interpolate,interpose,
interrogate,intersperse,intervene,intimate,intimidate,intone,intoxicate,intractable,
intransigent,introspective,introvert,intrude,intuition,inured,invalidate,inveigle,
inveigh,inventory,inverse,invert,invest,inveterate,invidious,invigorate,
invincible,inviolable,invoke,involuntary,ironic,irrational,irreconcilable,irrefutable,
irrelevant,irremediable,irreparable,irrepressible,irreproachable,irresistible,irretrievable,irreversible,
irrigate,irritate,isolate,issuance,iterate,
jaded,jarring,jaundiced,jaunt,jeer,jeopardize,jettison,jingoist,
jocose,jostle,jubilant,judicious,jumble,junction,jurisprudence,justify,
kaleidoscope,keen,kernel,keynote,kindle,kinetic,kith,knack,
knave,knead,knell,kudos,
lacerate,lachrymose,lackadaisical,lackluster,laggard,lambaste,lament,lampoon,
languish,lank,lapidary,larceny,largess,lascivious,lassitude,latent,
lateral,latitude,laudable,lavish,lax,layman,leaven,lecherous,
ledger,leery,legacy,legitimate,leniency,leonine,lesion,lethal,
levee,leverage,leviathan,lexicon,liable,liaison,libel,liberality,
libertine,licentious,lien,ligneous,lilliputian,limber,limn,limpid,
lineage,linger,lionize,liquidate,lissome,listless,literal,lithe,
litigation,livid,loath,loathe,lofty,logistics,longevity,lope,
lubricate,lucrative,lugubrious,lumber,luminary,lunar,lunge,lurid,
lurk,luscious,luster,lustrous,luxuriant,machination,magnate,magnitude,
maim,maladroit,malady,malaise,malapropism,malcontent,malediction,malefactor,
malicious,malinger,malleable,malodorous,mammoth,manacle,mandate,mandatory,
mangle,mania,maniacal,manifold,manipulate,mannered,manumit,mar,
marginal,marital,maritime,marquee,marshal,martial,martinet,marvel,
masochist,masticate,maternal,matriarch,matriculate,maudlin,maul,maverick,
mawkish,meager,meander,mediate,mediocre,medley,melancholy,mellifluous,
memento,memoir,menace,mendacious,mendicant,menial,mentor,mercenary,
mercurial,meretricious,merger,meridian,meritorious,mesmerize,metamorphosis,metaphor,
meteoric,methodical,meticulous,mettle,miasma,microcosm,milieu,militant,
militate,mimic,minatory,mincing,minion,minuscule,minutiae,misanthrope,
misapprehension,miscellany,mischievous,misconstrue,miscreant,misdemeanor,miser,miserly,
misgiving,mishap,misnomer,misogynist,missionary,missive,mite,mitigate
"""

# 추가 단어들 (2000개 맞추기 위해)
additional_words = """
modicum,modish,modulate,mogul,moiety,molest,mollify,molten,momentous,monetary,
monastic,mongrel,monochromatic,monolithic,monotony,monumental,moot,morbid,mordant,mores,
moribund,morose,morsel,mortify,motif,motley,mottled,mountebank,muddle,muffle,
mulct,multifarious,multitude,mundane,munificent,mural,murky,muse,muster,musty,
mutability,mute,mutilate,mutinous,mutter,myopic,myriad,mystique,naive,narcissist,
narrative,nascent,natal,natty,nauseate,navigate,nebulous,necessitate,necromancy,nefarious,
negate,negligence,nemesis,neologism,nepotism,nether,nettle,neutralize,nexus,nicety,
niggardly,nihilism,nimble,nirvana,nocturnal,noisome,nomadic,nomenclature,nominal,nonchalance,
noncommittal,nondescript,nonentity,nonpareil,nonplussed,nostalgia,notoriety,nourish,novice,noxious,
nuance,nubile,nugatory,nullify,numismatist,nurture,nutrient,oaf,obeisance,obese,
obfuscate,obituary,objurgate,oblation,obligatory,oblique,obliterate,oblivion,obloquy,obnoxious,
obscurantist,obsequies,observant,obsess,obsolete,obstreperous,obtrude,obtuse,obviate,occlude,
occult,odious,odium,odyssey,offhand,officious,offset,ogle,olfactory,oligarchy,
ominous,omnipotent,omniscient,omnivorous,onerous,onomatopoeia,onset,onslaught,onus,opaque,
operative,opiate,opportune,opprobrious,opprobrium,opt,optimal,optimist,opulence,opus,
oracle,oracular,oration,ordain,ordeal,ordinance,ornate,ornery,ornithology,orthodox,
oscillate,ossify,ostensible,ostentatious,ostracize,otiose,oust,outlandish,outmoded,outrage,
outskirts,outspoken,outwit,ovation,overbearing,overlap,overrule,oversight,overture,overwrought,
pachyderm,pacifist,paean,painstaking,palate,palatial,paleontology,palette,pall,palliate,
pallid,palpable,palpitate,paltry,panacea,panache,pandemic,pandemonium,pander,panegyric,
panorama,pantomime,papyrus,parable,paradigm,paragon,parallel,parameter,paramount,paranoia,
paraphernalia,paraphrase,parasite,parched,pariah,parity,parley,parlous,parochial,parody,
paroxysm,parquet,parry,parsimony,partial,partiality,partisan,parvenu,passivity,pastoral,
patent,paternal,pathetic,pathogen,pathos,patriarch,patrician,patrimony,patronage,patronize,
paucity,pauper,pavilion,peccadillo,peculate,pecuniary,pedagogue,pedant,pedestal,pedestrian,
pedigree,peer,peerless,peevish,pejorative,pellucid,penchant,pendant,pending,penetrate,
penitence,pennant,pensive,penumbra,penury,perambulate,perceive,perceptible,perceptive,percussion,
perdition,peregrination,peremptory,perennial,perfidy,perforate,perfunctory,peril,perimeter,peripheral,
peripatetic,perjury,permeate,permissive,pernicious,peroration,perpetrate,perpetual,perplex,perquisite,
persevere,persist,persona,personable,perspicacious,perspicuous,pertain,pertinacious,pertinent,perturb,
peruse,pervade,pervasive,perverse,pervert,pessimism,pestilence,petrous,petulant,phantom,
phenomenal,philanthropy,philippic,philistine,phlegmatic,phobia,phoenix,pied,piety,pigment,
pilfer,pillage,pillory,pine,pinion,pinnacle,pious,pique,pitfall,pith,
pithy,pittance,pivotal,placate,placebo,placid,plagiarize,plaintiff,plaintive,plait,
platitude,plaudit,plausible,plebeian,plebiscite,plenary,plenitude,plethora,pliable,pliant,
plight,plod,ploy,pluck,plumb,plummet,plunder,plutocracy,pneumatic,poach,
podiatrist,podium,poignant,polarize,polemic,politic,poll,polygamist,polyglot,pomposity,
ponderous,pontificate,pore,porous,portend,portent,portly,poseur,posterity,posthumous,
postulate,potable,potent,potentate,potion,potpourri,pragmatic,prattle,preamble,precarious
"""

# 모든 단어 합치기
all_words_raw = sat_words_raw + "," + additional_words
all_words = [w.strip() for w in all_words_raw.replace('\n', ',').split(',') if w.strip()]
all_words = list(set(all_words))  # 중복 제거

# 빈도수로 정렬하여 2000개 선택 (어려운 단어 우선)
word_freqs = [(w, word_frequency(w, 'en')) for w in all_words]
word_freqs.sort(key=lambda x: x[1])  # 낮은 빈도수 = 어려운 단어

# 상위 2000개 선택
words = [w for w, f in word_freqs[:2000]]
words.sort()

print(f'선택된 SAT 단어: {len(words)}개')
print(f'샘플: {words[:10]}')

# Gemini API 설정
API_KEY = 'AIzaSyCWW8OXnc7QwIUTs_W0FCEVrZEm3qliDzk'

def generate_word_data_batch(word_list):
    """word + POS 방식으로 영어 데이터 생성"""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'
    
    prompt = f"""Generate vocabulary data for SAT words: {', '.join(word_list)}

For EACH word, provide:
[
  {{
    "word": "aberration",
    "partOfSpeech": "noun",
    "definition": "a departure from what is normal or expected",
    "example": "The election results were an aberration caused by low voter turnout."
  }}
]

Rules:
- partOfSpeech: noun, verb, adjective, or adverb
- definition: Clear, concise definition for SAT level
- example: Natural academic sentence
- Return ONLY valid JSON array"""

    try:
        response = requests.post(url, json={
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'temperature': 0.3, 'maxOutputTokens': 8000}
        }, timeout=90)
        
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            text = text.strip()
            if text.startswith('```'):
                lines = text.split('\n')
                text = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
            if text.startswith('json'):
                text = text[4:]
            return json.loads(text)
    except Exception as e:
        print(f"  Error: {e}")
    return None

def translate_definitions_batch(definitions, target_lang):
    """정의를 대상 언어로 번역"""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'
    
    lang_names = {'ko': 'Korean', 'zh': 'Chinese', 'hi': 'Hindi'}
    
    prompt = f"""Translate these English definitions to {lang_names[target_lang]}. 
Give SHORT translations (1-3 words preferred), not full sentence translations.

{json.dumps(definitions, ensure_ascii=False)}

Return ONLY a JSON array of translated strings. No markdown."""

    try:
        response = requests.post(url, json={
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'temperature': 0.1, 'maxOutputTokens': 8000}
        }, timeout=90)
        
        if response.status_code == 200:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            text = text.strip()
            if text.startswith('```'):
                lines = text.split('\n')
                text = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
            if text.startswith('json'):
                text = text[4:]
            return json.loads(text)
    except Exception as e:
        print(f"  Translation error ({target_lang}): {e}")
    return None

# 1단계: 영어 데이터 생성
BATCH_SIZE = 20
all_word_data = []

print("\n===== 1단계: 영어 정의/예문 생성 =====")
for i in range(0, len(words), BATCH_SIZE):
    batch = words[i:i+BATCH_SIZE]
    print(f"  [{i+1}-{min(i+BATCH_SIZE, len(words))}/{len(words)}] 처리 중...")
    
    result = generate_word_data_batch(batch)
    if result:
        all_word_data.extend(result)
    else:
        # 실패 시 재시도
        time.sleep(2)
        result = generate_word_data_batch(batch)
        if result:
            all_word_data.extend(result)
        else:
            # 최종 실패 시 기본값
            for w in batch:
                all_word_data.append({
                    'word': w,
                    'partOfSpeech': 'noun',
                    'definition': f'{w} - SAT vocabulary word',
                    'example': f'The word {w} appears frequently on SAT exams.'
                })
    
    time.sleep(0.5)

print(f"\n영어 데이터 생성 완료: {len(all_word_data)}개")

# 2단계: 번역 추가 (ko, zh, hi)
languages = ['ko', 'zh', 'hi']

print("\n===== 2단계: 번역 생성 (3개 언어) =====")
for lang in languages:
    print(f"\n  {lang} 번역 중...")
    definitions = [w['definition'] for w in all_word_data]
    
    all_translations = []
    for i in range(0, len(definitions), 50):
        batch = definitions[i:i+50]
        print(f"    [{i+1}-{min(i+50, len(definitions))}/{len(definitions)}]")
        
        translations = translate_definitions_batch(batch, lang)
        if translations and len(translations) == len(batch):
            all_translations.extend(translations)
        else:
            # 실패 시 영어 유지
            all_translations.extend(batch)
        
        time.sleep(0.3)
    
    # 번역 적용
    for j, word_data in enumerate(all_word_data):
        if 'translations' not in word_data:
            word_data['translations'] = {}
        word_data['translations'][lang] = {
            'definition': all_translations[j] if j < len(all_translations) else word_data['definition']
        }

# 3단계: 난이도 배정 (빈도수 기반)
print("\n===== 3단계: 난이도 배정 =====")
for word_data in all_word_data:
    word_data['_freq'] = word_frequency(word_data['word'], 'en')

all_word_data.sort(key=lambda x: -x['_freq'])

n = len(all_word_data)
for i, word_data in enumerate(all_word_data):
    if i < n * 0.25:
        word_data['level'] = 'Basic'
    elif i < n * 0.50:
        word_data['level'] = 'Common'
    elif i < n * 0.75:
        word_data['level'] = 'Advanced'
    else:
        word_data['level'] = 'Expert'
    del word_data['_freq']

# ID 부여 및 정렬
all_word_data.sort(key=lambda x: x['word'])
for i, word_data in enumerate(all_word_data):
    word_data['id'] = i + 1

# 저장
output_path = r'C:\Users\hooni\Desktop\sat_vocab_app_new\assets\data\words.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_word_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 완료! {len(all_word_data)}개 단어 저장됨")
print(f"저장 위치: {output_path}")

# 레벨 분포
levels = Counter(w['level'] for w in all_word_data)
print(f"\n레벨 분포: {dict(levels)}")

# 샘플 출력
print("\n샘플 단어:")
sample = all_word_data[0]
print(f"  Word: {sample['word']}")
print(f"  POS: {sample['partOfSpeech']}")
print(f"  Definition: {sample['definition']}")
print(f"  Example: {sample['example']}")
print(f"  Korean: {sample['translations'].get('ko', {}).get('definition', 'N/A')}")
print(f"  Chinese: {sample['translations'].get('zh', {}).get('definition', 'N/A')}")
print(f"  Hindi: {sample['translations'].get('hi', {}).get('definition', 'N/A')}")
