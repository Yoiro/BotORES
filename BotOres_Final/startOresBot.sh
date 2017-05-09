echo "Start OresBot"  >> /volume1/share/BotORES/BotOres.log 2>&1
echo $(date) >> /volume1/share/BotORES/BotOres.log 2>&1
sudo docker run -v /volume1/share/BotORES/BotDownloads:/volume1/share/BotDownloads --rm botores python3 download_ores.py
