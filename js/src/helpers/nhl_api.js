async function getGamePlayByPlay(gameId) {
    const resp = await fetch(`https://api-web.nhle.com/v1/gamecenter/${gameId}/play-by-play`, { method: 'GET' });
    const data = await resp.json();
    return data;
}
const t = await getGamePlayByPlay('2023020204');
export { getGamePlayByPlay };
