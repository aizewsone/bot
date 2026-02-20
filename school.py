import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler, filters, 
                         ConversationHandler, ContextTypes)

logging.basicConfig(format="%(asftime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

clubs_data = {
    'club_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'name': [
        'Робототехника', 'рисование', 'Программирование', 'Биология',
        'Физика', 'индивидуальные виды спорта', 'игровые виды спорта', 
        'музыка', "шахматы", "химия"
    ],
    'math': [1, 0, 1, 0, 0.5, 0, 0, 0, 0.8, 0.3],
    'art': [0.4, 1, 0.4, 0, 0, 0, 0, 1, 0.1, 0],
    'social': [0.3, 0.2, 0.3, 0.2, 0, 0.3, 0.5, 0.7, 0.4, 0],
    'nature': [0, 0.5, 0, 0.5, 0.2, 0.4, 0.5, 0, 0, 0.4],
    'physical_activity': [0, 0, 0, 0, 0, 1, 1, 0.1, 0.2, 0],
    'science': [0, 0, 0.1, 1, 1, 0, 0, 0, 0, 1]   
}
clubs_df = pd.DataFrame(clubs_data)

# Состояния диалога
(QUESTION_MATH, QUESTION_ART, QUESTION_SOCIAL,
 QUESTION_NATURE, QUESTION_PHYSICAL, QUESTION_SCIENCE, QUESTION_INTERESTS) = range(7)

user_profiles = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_profiles[user_id] = {}
    await update.message.reply_text(" ХОББИБОТ👋 \n ПОМОЖЕТ УЗНАТЬ ВАМ, ЧТО ЛУЧШЕ ВЫБРАТЬ💭")
    await ask_math(update, context)
    return QUESTION_MATH

async def ask_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Как вы относитесь к математике🧮? (Оцените от 1 - совсем не нравится, до 5 - очень нравится)",
        reply_markup=reply_markup
    )

async def handle_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['math'] = value
            await ask_art(update, context)
            return QUESTION_ART
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_MATH
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_MATH

async def ask_art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Насколько вам нравится творчество🎨? (Оцените от 1 - совсем не нравится, до 5 - очень нравится)",
        reply_markup=reply_markup
    )

async def handle_art(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['art'] = value
            await ask_social(update, context)
            return QUESTION_SOCIAL
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_ART
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_ART

async def ask_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Насколько вы общительны💬? (Оцените от 1 - предпочитаю одиночество, до 5 - люблю общение)",
        reply_markup=reply_markup
    )

async def handle_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['social'] = value
            await ask_nature(update, context)
            return QUESTION_NATURE
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_SOCIAL
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_SOCIAL

async def ask_nature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Насколько вам интересна природа🌍? (оцените от 1 — совсем не нравится, до 5 — очень нравится)",
        reply_markup=reply_markup
    )

async def handle_nature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['nature'] = value
            await ask_physical(update, context)
            return QUESTION_PHYSICAL
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_NATURE
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_NATURE

async def ask_physical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Насколько вы активны физически🏃? (оцените от 1 — малоподвижный образ жизни, до 5 — высокая активность)",
        reply_markup=reply_markup
    )

async def handle_physical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['physical_activity'] = value
            await ask_science(update, context)
            return QUESTION_SCIENCE
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_PHYSICAL
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_PHYSICAL

async def ask_science(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2"],
        ["3", "4", "5"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Насколько вам интересна наука🔬? (оцените от 1 — совсем не нравится, до 5 — очень нравится)",
        reply_markup=reply_markup
    )

async def handle_science(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = int(update.message.text)
        if 1 <= value <= 5:
            user_id = update.effective_user.id
            user_profiles[user_id]['science'] = value
            await ask_interests(update, context)
            return QUESTION_INTERESTS
        else:
            await update.message.reply_text("Ошибка: нажмите кнопку")
            return QUESTION_SCIENCE
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_SCIENCE

async def ask_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7"]  
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    message = (
        "Отлично! Теперь расскажите, что вам особенно нравится:\n"
        "1 — компьютерные игры🎮\n"
        "2 — создавать что-то новое🖼\n"
        "3 — отдых на природе🍃\n"
        "4 — Спорт и активность🚴\n"
        "5 — коммуникация с людьми💬\n"
        "6 — исследования и эксперименты🔬\n"
        "7 — ничего из перечисленного😔\n\n"
    )
    await update.message.reply_text(message, reply_markup=reply_markup)

async def handle_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        user_input = update.message.text.strip()
        user_interests = [int(x.strip()) for x in user_input.split(',')]
        
        for interest in user_interests:
            if interest == 1:
                user_profiles[user_id]['math'] = min(user_profiles[user_id].get('math', 0) + 1, 5)
            elif interest == 2:
                user_profiles[user_id]['art'] = min(user_profiles[user_id].get('art', 0) + 1, 5)
            elif interest == 3:
                user_profiles[user_id]['nature'] = min(user_profiles[user_id].get('nature', 0) + 1, 5)
            elif interest == 4:
                user_profiles[user_id]['physical_activity'] = min(user_profiles[user_id].get('physical_activity', 0) + 1, 5)
            elif interest == 5:
                user_profiles[user_id]['social'] = min(user_profiles[user_id].get('social', 0) + 1, 5)
            elif interest == 6:
                user_profiles[user_id]['science'] = min(user_profiles[user_id].get('science', 0) + 1, 5)
        
        await show_results(update, context, user_id)
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("Ошибка: нажмите кнопку")
        return QUESTION_INTERESTS

def recommend_clubs(student_data, clubs_df):
    features = ['math', 'art', 'social', 'nature', 'physical_activity', 'science']
    
    student_vector = []
    for col in features:
        val = student_data.get(col, 0) / 5.0
        student_vector.append(val)
    
    club_vectors = clubs_df[features].values
    
    similarities = cosine_similarity([student_vector], club_vectors)[0]
    
    results_df = clubs_df.copy()
    results_df['score'] = similarities
    
    return results_df.sort_values(by='score', ascending=False)

async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):

    student_profile = user_profiles[user_id]
    
    recommendations = recommend_clubs(student_profile, clubs_df)
    

    best_match = recommendations.iloc[0]
    best_name = best_match['name']
    best_percentage = round(best_match['score'] * 100, 1)
    

    message = f"\n✅ АНАЛИЗ ЗАВЕРШЕН.\n\n"
    message += f"🎯 ЛУЧШЕЕ НАПРАВЛЕНИЕ ДЛЯ ВАС: {best_name}\n"
    message += f"📊 Соответствие профилю: {best_percentage}%\n\n"
    
    if best_percentage > 85:
        verdict = "✅ Идеальный выбор! Ваши способности и интересы полностью совпадают с программой."
    elif best_percentage > 60:
        verdict = "👍 Хороший вариант. Направления вам подходит, но может потребоваться освоение новых навыков."
    else:
        verdict = "🤔 Рекомендуется попробовать, но будьте готовы к тому, что это может быть непривычная сфера."
    
    message += f"🔍 ВЕРДИКТ ИИ: {verdict}\n\n"
    message += "🏆 ТОП-3 РЕКОМЕНДАЦИЙ:\n"
    
    # Формируем топ-3 рекомендаций
    top_3 = recommendations[['name', 'score']].head(3).copy()
    top_3['score'] = (top_3['score'] * 100).round(1)
    
    for i, (_, row) in enumerate(top_3.iterrows(), 1):
        stars = "⭐️" * int(row['score'] / 30)  # 1 звезда на каждые 30%
        message += f"{i}. {row['name']} - {row['score']}% {stars}\n"
    
    message += "\nЧтобы начать заново, отправьте команду /start"
    
    await update.message.reply_text(message)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог прерван. Чтобы начать заново, отправьте /start")
    return ConversationHandler.END

def main():
    application = Application.builder().token("8161871897:AAHifdIrr7iqKsLAccymjxb-OPJeYExlaQk").build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION_MATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_math)],
            QUESTION_ART: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_art)],
            QUESTION_SOCIAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_social)],
            QUESTION_NATURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_nature)],
            QUESTION_PHYSICAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_physical)],
            QUESTION_SCIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_science)],
            QUESTION_INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_interests)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    print("🤖 Бот запускается...")
    application.run_polling()

if __name__ == '__main__':  
    main()