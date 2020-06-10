--Для курсовой работы был выбран онлайн-кинотеатр Netflix.com:

CREATE DATABASE Netflix;

--По ходу знакомства с содержимым данного ресурса родилось следующее видение варианта реализации основной концепции хранилища данных:
--Основная сущность, вокруг которой крутятся все остальные - это Фильм(movies). 
--У каждого фильма есть: -ограничение по возрасту(age_limit), -категория(categories), -жанр(genres), -настроение(mood):

CREATE TABLE movies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  about VARCHAR(255),
  age_limit_id BIGINT UNSIGNED NOT NULL,
  category_id BIGINT UNSIGNED NOT NULL
);

CREATE TABLE age_limit (
  id SERIAL PRIMARY KEY,
  age_limit INT UNSIGNED NOT NULL
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  category VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE genres (
  id SERIAL PRIMARY KEY,
  genge VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE moods (
  id SERIAL PRIMARY KEY,
  mood VARCHAR(255) NOT NULL UNIQUE
);

--Нередко фильм может относиться к нескольким жанрам и настроениям:

CREATE TABLE movies_genres (
  movie_id BIGINT UNSIGNED NOT NULL,
  genre_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (movie_id, genre_id)
);

CREATE TABLE movies_moods (
  movie_id BIGINT UNSIGNED NOT NULL,
  mood_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (movie_id, mood_id)
);

--Т.к. Нетфликс - это ресурс, в основном, сериалов, то у каждого Фильма может быть несколько серий и сезонов (если полнометражка, то в полях 'season' и 'episode' будем ставить нули): 

CREATE TABLE movies_files (
  id SERIAL PRIMARY KEY,
  movie_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR(255),
  about VARCHAR(255),
  season INT UNSIGNED NOT NULL,
  episode INT UNSIGNED NOT NULL,
  duration INT UNSIGNED NOT NULL,
  metadata VARCHAR(255)  
);

--Тажке очень важная сущность - это Человек, Человек может быть как простым пользователем-зрителем Нетфликса, так и актером или создателем (продюсер, режиссер).
--чтобы не городить много таблиц, будем хранить всех "Человеков" в одной таблице:

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  s_name VARCHAR(255) 
);

--А для зрителей будем хранить профили с информацией об: -пин-код для родительского контроля(pc_pin), -план доступа к фильмам(plan_id), инфо об оплате подписки(payment_info), родительский контроль(maturity_id):  

CREATE TABLE profiles (
  id SERIAL PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  passwd VARCHAR(50) NOT NULL,
  pc_pin INT UNSIGNED,  
  email VARCHAR(100) NOT NULL UNIQUE,
  phone VARCHAR(100) NOT NULL UNIQUE,
  reg_date DATETIME DEFAULT NOW(),
  plan_id BIGINT UNSIGNED NOT NULL,
  payment_info VARCHAR(100),
  billing_details VARCHAR(100),
  maturity_id BIGINT UNSIGNED NOT NULL
);

CREATE TABLE plans (
  id SERIAL PRIMARY KEY,
  plan VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE maturity (
  id SERIAL PRIMARY KEY,
  maturity VARCHAR(50) NOT NULL UNIQUE
);

-- А актеров и создателей в таблицах:

CREATE TABLE movies_actors (
  user_id BIGINT UNSIGNED NOT NULL,
  movie_file_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, movie_file_id)
);

CREATE TABLE movies_creaters (
  user_id BIGINT UNSIGNED NOT NULL,
  movie_file_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, movie_file_id)
);

-- Очень важны на Нетфликсе (как я понимаю, например, для формирования портрета зрителя или для выявления top-фильмов) истории просмотра контента каждым зрителем и им проставленные лайки/дислайки:

CREATE TABLE activities (
  id SERIAL PRIMARY KEY,
  profile_id BIGINT UNSIGNED NOT NULL,
  movie_file_id BIGINT UNSIGNED NOT NULL,
  visited_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rating (
  profile_id BIGINT UNSIGNED NOT NULL,
  movie_file_id BIGINT UNSIGNED NOT NULL,
  like_kind_id BIGINT UNSIGNED NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (profile_id, movie_file_id)
);

CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  like_kind VARCHAR(10) NOT NULL UNIQUE
);

-- Далее по коду таблиц сгенерируем данные на http://filldb.info/
-- Исходник на потабличную заливку данных - filldb2.info  

-- Организуем межтабличные связи:   

ALTER TABLE profiles
  ADD CONSTRAINT profiles_user_id_fk
    FOREIGN KEY (user_id) REFERENCES users(id),
  ADD CONSTRAINT profiles_plan_id_fk
    FOREIGN KEY (plan_id) REFERENCES plans(id),      
  ADD CONSTRAINT profiles_maturity_id_fk
    FOREIGN KEY (maturity_id) REFERENCES maturity(id)
;	 

ALTER TABLE movies
  ADD CONSTRAINT movies_age_limit_id_fk
    FOREIGN KEY (age_limit_id) REFERENCES age_limit(id),
  ADD CONSTRAINT movies_categories_id_fk
    FOREIGN KEY (category_id) REFERENCES categories(id)  
;

ALTER TABLE movies_genres
  ADD CONSTRAINT movies_genres_movie_id_fk
    FOREIGN KEY (movie_id) REFERENCES movies(id),
  ADD CONSTRAINT movies_genres_genre_id_fk
    FOREIGN KEY (genre_id) REFERENCES genres(id)  
;

ALTER TABLE movies_moods
  ADD CONSTRAINT movies_moods_movie_id_fk
    FOREIGN KEY (movie_id) REFERENCES movies(id),
  ADD CONSTRAINT movies_moods_genre_id_fk
    FOREIGN KEY (mood_id) REFERENCES moods(id)  
;

ALTER TABLE movies_files
  ADD CONSTRAINT movies_files_movie_id_fk
    FOREIGN KEY (movie_id) REFERENCES movies(id)
;

ALTER TABLE movies_actors
  ADD CONSTRAINT aclors_users_user_id_fk
    FOREIGN KEY (user_id) REFERENCES users(id),
  ADD CONSTRAINT movies_users_role_id_fk
    FOREIGN KEY (movie_file_id) REFERENCES movies_files(id)
;

ALTER TABLE movies_creaters
  ADD CONSTRAINT movies_creators_user_id_fk
    FOREIGN KEY (user_id) REFERENCES users(id),
  ADD CONSTRAINT movies_creators_role_id_fk
    FOREIGN KEY (movie_file_id) REFERENCES movies_files(id)
;

ALTER TABLE activities
  ADD CONSTRAINT activities_profile_id_fk
    FOREIGN KEY (profile_id) REFERENCES profiles(id),
  ADD CONSTRAINT activities_movie_files_id_fk
    FOREIGN KEY (movie_file_id) REFERENCES movies_files(id)
;

ALTER TABLE rating
  ADD CONSTRAINT rating_movie_files_id_fk
    FOREIGN KEY (movie_file_id) REFERENCES movies_files(id),
  ADD CONSTRAINT rating_like_kind_id_fk
    FOREIGN KEY (like_kind_id) REFERENCES likes(id),
  ADD CONSTRAINT rating_profile_id_fk
    FOREIGN KEY (profile_id) REFERENCES profiles(id)
;















































