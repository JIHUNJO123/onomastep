import 'package:flutter/material.dart';
import 'package:onoma_step_app/l10n/generated/app_localizations.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../services/ad_service.dart';
import '../services/display_service.dart';
import 'word_list_screen.dart';
import 'word_detail_screen.dart';
import 'favorites_screen.dart';
import 'quiz_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Word? _todayWord;
  String? _translatedDefinition;
  bool _isLoading = true;
  bool _isBannerAdLoaded = false;
  String? _lastLanguage;
  List<String> _categories = [];

  // 카테고리 번역 함수
  String _getLocalizedCategory(String category, AppLocalizations l10n) {
    // 카테고리명을 키로 변환 (공백과 특수문자 제거)
    final key = category.replaceAll(RegExp(r'[/\s]'), '');
    
    switch (key) {
      case 'AnimalSounds': return l10n.cat_AnimalSounds;
      case 'HumanSounds': return l10n.cat_HumanSounds;
      case 'ImpactSounds': return l10n.cat_ImpactSounds;
      case 'WaterLiquidSounds': return l10n.cat_WaterLiquidSounds;
      case 'MechanicalSounds': return l10n.cat_MechanicalSounds;
      case 'WindAirSounds': return l10n.cat_WindAirSounds;
      case 'OtherSounds': return l10n.cat_OtherSounds;
      case 'WalkingRunning': return l10n.cat_WalkingRunning;
      case 'JumpingBouncing': return l10n.cat_JumpingBouncing;
      case 'ShakingSwaying': return l10n.cat_ShakingSwaying;
      case 'SpinningRolling': return l10n.cat_SpinningRolling;
      case 'SlidingSlipping': return l10n.cat_SlidingSlipping;
      case 'FastQuick': return l10n.cat_FastQuick;
      case 'SlowLeisurely': return l10n.cat_SlowLeisurely;
      case 'OtherMotion': return l10n.cat_OtherMotion;
      case 'PositiveEmotions': return l10n.cat_PositiveEmotions;
      case 'NegativeEmotions': return l10n.cat_NegativeEmotions;
      case 'AnxietyNervousness': return l10n.cat_AnxietyNervousness;
      case 'HeartbeatExcitement': return l10n.cat_HeartbeatExcitement;
      case 'Confident': return l10n.cat_Confident;
      case 'ShyHesitant': return l10n.cat_ShyHesitant;
      case 'LazyCareless': return l10n.cat_LazyCareless;
      case 'FatigueSleepiness': return l10n.cat_FatigueSleepiness;
      case 'OtherEmotions': return l10n.cat_OtherEmotions;
      case 'PainDiscomfort': return l10n.cat_PainDiscomfort;
      case 'HungerFullness': return l10n.cat_HungerFullness;
      case 'Chewing': return l10n.cat_Chewing;
      case 'Drinking': return l10n.cat_Drinking;
      case 'OtherEating': return l10n.cat_OtherEating;
      case 'LightShine': return l10n.cat_LightShine;
      case 'Temperature': return l10n.cat_Temperature;
      case 'WetDry': return l10n.cat_WetDry;
      case 'SoftHard': return l10n.cat_SoftHard;
      case 'StickySlippery': return l10n.cat_StickySlippery;
      case 'CleanMessy': return l10n.cat_CleanMessy;
      case 'Shape': return l10n.cat_Shape;
      case 'Size': return l10n.cat_Size;
      case 'Abundance': return l10n.cat_Abundance;
      case 'Scarcity': return l10n.cat_Scarcity;
      case 'RainSnow': return l10n.cat_RainSnow;
      case 'Wind': return l10n.cat_Wind;
      case 'OtherWeather': return l10n.cat_OtherWeather;
      case 'Others': return l10n.cat_Others;
      default: return category;
    }
  }

  // 카테고리별 아이콘 매핑
  IconData _getCategoryIcon(String category) {
    switch (category) {
      case 'Animal Sounds': return Icons.pets;
      case 'Human Sounds': return Icons.person;
      case 'Impact Sounds': return Icons.sports_martial_arts;
      case 'Water/Liquid Sounds': return Icons.water_drop;
      case 'Mechanical Sounds': return Icons.settings;
      case 'Wind/Air Sounds': return Icons.air;
      case 'Other Sounds': return Icons.volume_up;
      case 'Walking/Running': return Icons.directions_walk;
      case 'Jumping/Bouncing': return Icons.sports_basketball;
      case 'Shaking/Swaying': return Icons.vibration;
      case 'Spinning/Rolling': return Icons.rotate_right;
      case 'Sliding/Slipping': return Icons.sledding;
      case 'Fast/Quick': return Icons.speed;
      case 'Slow/Leisurely': return Icons.hourglass_bottom;
      case 'Other Motion': return Icons.directions_run;
      case 'Positive Emotions': return Icons.sentiment_very_satisfied;
      case 'Negative Emotions': return Icons.sentiment_very_dissatisfied;
      case 'Anxiety/Nervousness': return Icons.psychology;
      case 'Heartbeat/Excitement': return Icons.favorite;
      case 'Confident': return Icons.thumb_up;
      case 'Shy/Hesitant': return Icons.face;
      case 'Lazy/Careless': return Icons.weekend;
      case 'Fatigue/Sleepiness': return Icons.hotel;
      case 'Other Emotions': return Icons.emoji_emotions;
      case 'Pain/Discomfort': return Icons.healing;
      case 'Hunger/Fullness': return Icons.restaurant;
      case 'Chewing': return Icons.dining;
      case 'Drinking': return Icons.local_drink;
      case 'Other Eating': return Icons.fastfood;
      case 'Light/Shine': return Icons.wb_sunny;
      case 'Temperature': return Icons.thermostat;
      case 'Wet/Dry': return Icons.opacity;
      case 'Soft/Hard': return Icons.layers;
      case 'Sticky/Slippery': return Icons.water;
      case 'Clean/Messy': return Icons.cleaning_services;
      case 'Shape': return Icons.category;
      case 'Size': return Icons.straighten;
      case 'Abundance': return Icons.inventory;
      case 'Scarcity': return Icons.remove_circle_outline;
      case 'Rain/Snow': return Icons.umbrella;
      case 'Wind': return Icons.wind_power;
      case 'Other Weather': return Icons.cloud;
      case 'Others': return Icons.more_horiz;
      default: return Icons.label;
    }
  }

  Color _getCategoryColor(int index) {
    final colors = [
      Colors.blue, Colors.green, Colors.orange, Colors.pink,
      Colors.purple, Colors.red, Colors.teal, Colors.indigo,
      Colors.amber, Colors.cyan, Colors.lime, Colors.deepOrange,
    ];
    return colors[index % colors.length];
  }

  @override
  void initState() {
    super.initState();
    _loadTodayWord();
    _loadCategories();
    _loadBannerAd();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final currentLanguage = TranslationService.instance.currentLanguage;
    if (_lastLanguage != null && _lastLanguage != currentLanguage) {
      _loadTodayWord();
    }
    _lastLanguage = currentLanguage;
  }

  Future<void> _loadCategories() async {
    final categories = await DatabaseHelper.instance.getAllCategories();
    if (mounted) {
      setState(() {
        _categories = categories;
      });
    }
  }

  Future<void> _loadBannerAd() async {
    final adService = AdService.instance;
    await adService.initialize();

    if (!adService.adsRemoved) {
      await adService.loadBannerAd(
        onLoaded: () {
          if (mounted) {
            setState(() {
              _isBannerAdLoaded = true;
            });
          }
        },
      );
    }
  }

  Future<void> _loadTodayWord() async {
    try {
      final word = await DatabaseHelper.instance.getTodayWord();
      if (word != null) {
        final translationService = TranslationService.instance;
        await translationService.init();

        if (translationService.needsTranslation) {
          final embeddedTranslation = word.getEmbeddedTranslation(
            translationService.currentLanguage,
            'definition',
          );

          if (mounted) {
            setState(() {
              _todayWord = word;
              _translatedDefinition = embeddedTranslation;
              _isLoading = false;
            });
          }
        } else {
          if (mounted) {
            setState(() {
              _todayWord = word;
              _translatedDefinition = null;
              _isLoading = false;
            });
          }
        }
      } else {
        if (mounted) {
          setState(() {
            _todayWord = null;
            _isLoading = false;
          });
        }
      }
    } catch (e) {
      print('Error loading today word: $e');
      if (mounted) {
        setState(() {
          _todayWord = null;
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    AdService.instance.disposeBannerAd();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          l10n.appTitle,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildTodayWordCard(),
                  const SizedBox(height: 24),
                  Text(
                    l10n.learning,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildMenuGrid(),
                  const SizedBox(height: 24),
                  Text(
                    l10n.levelLearning,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildCategoryCards(),
                ],
              ),
            ),
          ),
          _buildBannerAd(),
        ],
      ),
    );
  }

  Widget _buildBannerAd() {
    final adService = AdService.instance;

    if (adService.adsRemoved ||
        !_isBannerAdLoaded ||
        adService.bannerAd == null) {
      return const SizedBox.shrink();
    }

    return Container(
      width: adService.bannerAd!.size.width.toDouble(),
      height: adService.bannerAd!.size.height.toDouble(),
      alignment: Alignment.center,
      child: AdWidget(ad: adService.bannerAd!),
    );
  }

  Widget _buildTodayWordCard() {
    final l10n = AppLocalizations.of(context)!;

    if (_isLoading) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Center(child: CircularProgressIndicator()),
        ),
      );
    }

    if (_todayWord == null) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Center(child: Text(l10n.cannotLoadWords)),
        ),
      );
    }

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => WordDetailScreen(word: _todayWord!),
            ),
          );
        },
        borderRadius: BorderRadius.circular(16),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(24.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            gradient: LinearGradient(
              colors: [
                Theme.of(context).primaryColor,
                Theme.of(context).primaryColor.withAlpha((0.7 * 255).toInt()),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: Colors.white.withAlpha((0.2 * 255).toInt()),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  "\u{1F4C5} ${l10n.todayWord}",
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Text(
                _todayWord!.word,
                style: const TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
              if (_todayWord!.hiragana != null && _todayWord!.hiragana != _todayWord!.word)
                Text(
                  _todayWord!.hiragana!,
                  style: const TextStyle(
                    fontSize: 16,
                    color: Colors.white70,
                  ),
                ),
              const SizedBox(height: 12),
              Text(
                _translatedDefinition ?? _todayWord!.definition,
                style: const TextStyle(fontSize: 16, color: Colors.white),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuGrid() {
    final l10n = AppLocalizations.of(context)!;

    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 1.3,
      children: [
        _buildMenuCard(
          icon: Icons.list_alt,
          title: l10n.allWords,
          subtitle: l10n.viewAllWords,
          color: Colors.blue,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const WordListScreen()),
            );
          },
        ),
        _buildMenuCard(
          icon: Icons.favorite,
          title: l10n.favorites,
          subtitle: l10n.savedWords,
          color: Colors.red,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const FavoritesScreen()),
            );
          },
        ),
        _buildMenuCard(
          icon: Icons.style,
          title: l10n.flashcard,
          subtitle: l10n.cardLearning,
          color: Colors.orange,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const WordListScreen(isFlashcardMode: true),
              ),
            );
          },
        ),
        _buildMenuCard(
          icon: Icons.quiz,
          title: l10n.quiz,
          subtitle: l10n.testYourself,
          color: Colors.green,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const QuizScreen()),
            );
          },
        ),
      ],
    );
  }

  Widget _buildMenuCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 10.0),
          child: Row(
            children: [
              Icon(icon, size: 36, color: color),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      subtitle,
                      style: TextStyle(color: Colors.grey[600], fontSize: 11),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryCards() {
    final l10n = AppLocalizations.of(context)!;
    
    if (_categories.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    return SizedBox(
      height: 100,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: _categories.length,
        itemBuilder: (context, index) {
          final category = _categories[index];
          final localizedCategory = _getLocalizedCategory(category, l10n);
          final color = _getCategoryColor(index);
          final icon = _getCategoryIcon(category);

          return Container(
            width: 100,
            margin: const EdgeInsets.only(right: 10),
            child: Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: InkWell(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => WordListScreen(level: category),
                    ),
                  );
                },
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    gradient: LinearGradient(
                      colors: [
                        color.withAlpha((0.8 * 255).toInt()),
                        color,
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        icon,
                        color: Colors.white,
                        size: 28,
                      ),
                      const SizedBox(height: 8),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 4),
                        child: Text(
                          localizedCategory,
                          style: const TextStyle(
                            fontSize: 9,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
