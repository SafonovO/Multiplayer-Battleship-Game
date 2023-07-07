'''
CITATION: I got this button class from a youtube video 

https://www.youtube.com/watch?v=GMBqjxcKogA&embeds_referring_euri=
https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dbuild%2Bmenu%2Bin%2Bpygame%
26rlz%3D1C1CHBF_enCA923CA923%26oq%3Dbuild%2Bmenu%2Bin%2Bpygame%26aqs%3D
chrome..69i57.2316j0j4&source_ve_path=Mjg2NjY&feature=emb_logo&ab_channel=
BaralTech

Which linked to this git repo:

https://github.com/baraltech/Menu-System-PyGame

From there, I took the Button class that is found in this file
'''
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)