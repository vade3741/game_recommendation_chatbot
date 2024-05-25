import gplay from 'google-play-scraper';
import { createWriteStream, mkdirSync, existsSync } from 'fs';
import { dirname } from 'path';

const categories = [
    'GAME', 'GAME_ACTION', 'GAME_ADVENTURE', 'GAME_ARCADE', 'GAME_BOARD', 'GAME_CARD',
    'GAME_CASINO', 'GAME_CASUAL', 'GAME_EDUCATIONAL', 'GAME_MUSIC', 'GAME_PUZZLE', 'GAME_RACING',
    'GAME_ROLE_PLAYING', 'GAME_SIMULATION', 'GAME_SPORTS', 'GAME_STRATEGY', 'GAME_TRIVIA', 'GAME_WORD'
];

const collections = ['TOP_FREE'];

const ensureDirectoryExistence = (filePath) => {
    const dir = dirname(filePath);
    if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
    }
};

const writeGameDetails = (file, games, category) => {
    games.forEach(game => {
        const line = `"${game.title}","${game.appId}","${game.summary.replace(/"/g, '""')}","${game.icon}","${category}"\n`;
        file.write(line);
    });
};

for (let col of collections) {
    for (let cat of categories) {
        const filePath = `./Data/google_games/AppID_${col}_${cat}.csv`;
        ensureDirectoryExistence(filePath);
        const file = createWriteStream(filePath);

        // Write CSV header
        file.write('Game Name,Package Name,Description,Icon URL,Category\n');

        gplay.list({
            category: gplay.category[cat],
            collection: gplay.collection[col],
            num: 100 // Adjust number if needed
        })
        .then(result => writeGameDetails(file, result, cat))
        .catch(error => console.error(`Error fetching apps for category ${cat} and collection ${col}:`, error));
    }
}
