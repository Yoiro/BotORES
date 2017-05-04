echo "Start OresBot"  >> /volume1/share/BotORES/BotOres.log 2>&1
echo $(date) >> /volume1/share/BotORES/BotOres.log 2>&1
docker run -v /volume1/share/BotORES/BotDownloads:/volume1/share/BotDownloads --rm oresbot python download_ores.py
