import * as nhl_api from './helpers/nhl_api.js';
const a = await nhl_api.getGamePlayByPlay('2023020204');
for (let play of a.plays) {
    console.log(play);
}
