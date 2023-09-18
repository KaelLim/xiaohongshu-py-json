    $(document).ready(function() {
        // Fetch the data from GitHub
        $.getJSON('https://raw.githubusercontent.com/KaelLim/xiaohongshu-py-json/main/video_details.json', function(data) {
            data.forEach(video => {
                const videoItem = `
                <div class="video-item">
                    <img src="${video.image_links[0]}" data-fancybox href="${video.video_url}" alt="Thumbnail">
                    <div>
                        <h3>${video.title}</h3>
                        <p>${video.description}</p>
                    </div>
                </div>
                `;
                $('#video-feed').append(videoItem);
            });
        });
    });