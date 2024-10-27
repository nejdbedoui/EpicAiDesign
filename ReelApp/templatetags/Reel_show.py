import base64
import io
import tempfile
from PIL import Image, ImageDraw, ImageFont
from django import template
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def show_reel(reel):
    try:
        clips = []

        # Handle video clip
        if reel.video:
            video_clip = VideoFileClip(reel.video.video_file)
            clips.append(video_clip)

        # Handle image clip
        if reel.image:
            image_file = reel.image.image.read()  # Read image data
            # Create a temporary file for the image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
                temp_image.write(image_file)
                temp_image_path = temp_image.name

            image_clip = ImageClip(temp_image_path).set_duration(5)
            clips.append(image_clip)

        # Handle poem as a text overlay
        if reel.poem:
            poem_text = reel.poem.text
            background_image_path = "background_image.jpg"  # Path to the background image

            # Create a new image with the poem text
            # Load background image
            background = ImageClip(background_image_path).get_frame(0)  # Get a frame from the background image

            # Prepare to draw on the background
            txt = Image.new('RGBA', background.size, (255, 255, 255, 0))  # Transparent overlay
            draw = ImageDraw.Draw(txt)

            # Define font (you may need to adjust the path and size)
            font_size = 30  # Adjust as needed
            font = ImageFont.truetype("arial.ttf", font_size)  # Load your font
            text_width, text_height = draw.textsize(poem_text, font)

            # Center the text
            x = (background.width - text_width) / 2
            y = (background.height - text_height) / 2

            # Draw the text on the transparent overlay
            draw.text((x, y), poem_text, font=font, fill=(255, 255, 255, 255))  # White text

            # Combine background with text
            combined = Image.alpha_composite(Image.fromarray(background), txt)
            combined.save("poem_overlay.png")  # Save overlay as an image

            # Create ImageClip from the combined image
            poem_image_clip = ImageClip("poem_overlay.png").set_duration(5)
            clips.append(poem_image_clip)

        # Create the final composite video
        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")

            # Handle audio track
            if reel.track:
                encoded_string = base64.b64encode(reel.track.audio.read()).decode('utf-8')

                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                    temp_audio.write(encoded_string)
                    temp_audio_path = temp_audio.name

                # Create an AudioFileClip from the temporary audio file
                audio_clip = AudioFileClip(temp_audio_path)
                final_clip = final_clip.set_audio(audio_clip)
            # Handle speech audio
            elif reel.speech:
                speech_audio_clip = AudioFileClip(reel.speech.speech_file)  # Assuming speech_file points to an audio file
                final_clip = final_clip.set_audio(speech_audio_clip)

            # Write the final video to a byte stream
            video_output = io.BytesIO()
            final_clip.write_videofile(video_output, codec="libx264")
            video_output.seek(0)

            encoded_video = base64.b64encode(video_output.read()).decode("utf-8")
            video_html = f'<video controls><source src="data:video/mp4;base64,{encoded_video}" type="video/mp4"></video>'
            print(video_html)
            return mark_safe(video_html)

        else:
            return "No content available in reel."

    except Exception as e:
        print(f"Error showing reel: {e}")
        return ""
