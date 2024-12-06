import pygame
import time
import math

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
green = (102, 204, 102)  # More natural green
grey = (128, 128, 128)  # Grey road
yellow = (255, 255, 0)  # Yellow dashed lines
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)  # Orange for stall out screen

# Load car image
car_image = pygame.image.load("updatedcar.png")
car_rect = car_image.get_rect(center=(screen_width // 2, screen_height - 50))

# Gear variables
current_gear = 0  # Start in Neutral gear
clutch_engaged = False

# RPM and Speed
rpm = 1000  # Starting RPM in Neutral
speed = 0

# Time variables for acceleration and clutch
last_acceleration_time = time.time()
last_clutch_time = time.time()
clutch_engaged_timer = 0

# Acceleration constants (adjust these for different car behaviors)
acceleration_rates = {
    1: 0.2,  # Acceleration rate in 1st gear (mph per 0.5 seconds)
    2: 1.0,  # Acceleration rate in 2nd gear
    3: 1.5,  # Acceleration rate in 3rd gear
    4: 5.0,  # Acceleration rate in 4th gear
    5: 7.5,  # Acceleration rate in 5th gear (range: 7-10 mph per 0.5 seconds)
}

# Road width and other constants
road_width = 400  # Road width doubled
line_width = 10
line_spacing = 50

# Road position
road_x = 0
road_y = screen_height // 2 - road_width // 2

# Yellow line position (start at the top and keep track of where each line is)
line_positions = []
for i in range(0, screen_height, line_spacing * 2):
    line_positions.append(i)

# Game loop
running = True
game_over = False
while running:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            # Implement car acceleration (with realistic acceleration)
            current_time = time.time()
            if current_time - last_acceleration_time >= 0.5:  # Changed to half a second
                last_acceleration_time = current_time
                if current_gear in acceleration_rates:
                    acceleration_rate = acceleration_rates[current_gear]
                    speed += acceleration_rate  # Apply acceleration based on gear

                # Update RPM based on acceleration
                if current_gear == 1:
                    # If RPM drops below 1000 in 1st gear, bring it back up
                    if rpm < 1000:
                        rpm = 1000
                    else:
                        rpm += 50  # Otherwise, increase RPM normally
                    print("RPM in 1st gear:", rpm)  # Added debug print
                elif current_gear == 2:
                    rpm += 100
                    print("RPM in 2nd gear:", rpm)  # Added debug print
                elif current_gear == 3:
                    rpm += 150
                    print("RPM in 3rd gear:", rpm)  # Added debug print
                elif current_gear == 4:
                    rpm += 200
                    print("RPM in 4th gear:", rpm)  # Added debug print
                elif current_gear == 5:
                    rpm += 250
                    print("RPM in 5th gear:", rpm)  # Added debug print

                # Limit speed (adjust based on gear)
                if current_gear == 1:
                    if speed > 10:
                        speed = 10
                elif current_gear == 2:
                    if speed > 30:
                        speed = 30
                elif current_gear == 3:
                    if speed > 60:
                        speed = 60
                elif current_gear == 4:
                    if speed > 100:
                        speed = 100
                elif current_gear == 5:
                    if speed > 150:
                        speed = 150

        if keys[pygame.K_DOWN]:
            # Implement car deceleration (simplified)
            if speed > 0:  # Only decelerate if the car is moving forward
                speed -= 2
                rpm -= 25
                if rpm < 0:
                    rpm = 0

        # Clutch handling
        if keys[pygame.K_c]:
            clutch_engaged = True
            # RPM should not drop below 1000 in 1st gear
            if current_gear == 1:
                current_time = time.time()
                if current_time - last_acceleration_time >= 1:  # Check for 1 second interval
                    last_acceleration_time = current_time
                    rpm -= 50  # Reduce RPM by 50 per second
                    if rpm < 1000:
                        rpm = 1000  # Clamp RPM to 1000
                # Speed decrease only in 1st gear with clutch engaged
                clutch_engaged_timer += current_time - last_clutch_time
                last_clutch_time = current_time
                if clutch_engaged_timer <= 2:
                    speed -= 0.25
                    if speed < 0:
                        speed = 0
                else:
                    speed = 0
            elif current_gear != 0:  # If not already in neutral
                # Reduce speed and RPM when clutch is engaged
                speed -= 0.5
                if rpm > 100:  # Only dip RPM by 100 max
                    rpm = rpm - 100  # Dip RPM by 100
                if speed < 0:
                    speed = 0
        else:
            clutch_engaged = False
            clutch_engaged_timer = 0

        # Gear shifting (with speed restrictions and RPM handling)
        if clutch_engaged:
            previous_gear = current_gear
            if keys[pygame.K_1]:
                current_gear = 1
                if previous_gear > 1:
                    if previous_gear == 2:
                        rpm += 250  # Small RPM spike for 2-1 downshift
                    else:
                        rpm += 750  # Moderate RPM spike for multi-gear downshift
            if keys[pygame.K_2] and rpm >= 300:  # Allow shifting to 2nd gear even if RPM is below 1000
                current_gear = 2
                if previous_gear > 2:
                    if previous_gear == 3:
                        rpm += 250  # Small RPM spike for 3-2 downshift
                    else:
                        rpm += 750  # Moderate RPM spike for multi-gear downshift
            if keys[pygame.K_3] and speed >= 10:  # 3rd gear only after 10 mph
                current_gear = 3
                if previous_gear > 3:
                    if previous_gear == 4:
                        rpm += 250  # Small RPM spike for 4-3 downshift
                    else:
                        rpm += 750  # Moderate RPM spike for multi-gear downshift
            if keys[pygame.K_4] and speed >= 30:  # 4th gear only after 30 mph
                current_gear = 4
                if previous_gear > 4:
                    if previous_gear == 5:
                        rpm += 250  # Small RPM spike for 5-4 downshift
                    else:
                        rpm += 750  # Moderate RPM spike for multi-gear downshift
            if keys[pygame.K_5] and speed >= 60:  # 5th gear only after 60 mph
                current_gear = 5
                if previous_gear > 5:
                    rpm += 750  # Moderate RPM spike for multi-gear downshift
            if keys[pygame.K_n]:  # Neutral gear
                current_gear = 0
                if previous_gear != 0:
                    rpm -= 250  # Small RPM drop for shifting to neutral

            # Upshift RPM behavior (slight decrease)
            if previous_gear < current_gear:
                if previous_gear == 1 and current_gear == 2:
                    rpm -= 100  # Reduced RPM decrease for 1-2 upshift
                else:
                    rpm -= 100

        # Ensure speed doesn't go negative
        if speed < 0:
            speed = 0

        # Check for engine stall (RPM below 500 in 1st gear, below 300 in other gears)
        if current_gear == 1 and rpm < 500:
            game_over = True
        elif current_gear != 1 and rpm < 300 and current_gear != 0:
            game_over = True

        # Check for engine explosion (RPM above 10000)
        if rpm > 10000 and current_gear != 0:  # Added check for neutral gear
            game_over = True

        # Draw elements
        screen.fill(grey)  # Fill background with grey

        # Draw the road (horizontal with dashed lines)
        pygame.draw.rect(screen, grey, (0, road_y, screen_width, road_width))

        # Move lines down based on speed
        line_speed_multiplier = 1  # Default multiplier
        if current_gear == 1 or current_gear == 2:
            line_speed_multiplier = 1.5  # Make it 1.5 times faster in 1st gear
        for i in range(len(line_positions)):
            line_positions[i] += int(speed * 0.2 * line_speed_multiplier)

            # Draw line if it's within the screen bounds
            if 0 <= line_positions[i] <= screen_height:
                pygame.draw.rect(screen, yellow, (screen_width // 2 - line_width // 2, line_positions[i], line_width, line_spacing))

            # If a line goes off the bottom, create a new line at the top
            if line_positions[i] >= screen_height:
                line_positions[i] = line_positions[i] - screen_height - line_spacing  # Reset the line position to above the screen

        # Draw the car in the center
        screen.blit(car_image, car_rect)

        # Keep car in center of the screen (infinite scrolling)
        if car_rect.x < 0:
            car_rect.x = 0
        elif car_rect.x > screen_width - car_rect.width:
            car_rect.x = screen_width - car_rect.width

        # Display current gear
        font = pygame.font.Font(None, 36)
        gear_text = font.render(f"Gear: {'N' if current_gear == 0 else current_gear}", True, (255, 255, 255))
        screen.blit(gear_text, (10, 10))

        # Display RPM and Speed gauges
        rpm_text = font.render(f"RPM: {rpm}", True, (255, 255, 255))
        speed_text = font.render(f"Speed: {speed:.1f}", True, (255, 255, 255))
        screen.blit(rpm_text, (10, 50))
        screen.blit(speed_text, (10, 90))

        # Move car left and right
        if keys[pygame.K_LEFT]:
            car_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            car_rect.x += 5

        # Update speed minimum in Neutral (N) to 0
        if current_gear == 0:
            if speed < 0:
                speed = 0
        # Update speed minimum in 1st gear to 5
        if current_gear == 1:
            if speed < 5:
                speed = 5
        # Update speed minimum in other gears to 0
        if current_gear > 1:
            if speed < 0:
                speed = 0

        pygame.display.flip()  # Update display
    else:
        # Game Over screen (Engine Stall or Explosion)
        if rpm > 10000:
            screen.fill(red)
            game_over_text = font.render("GAME OVER! Engine Exploded!", True, (255, 255, 255))
        else:
            screen.fill(orange)
            game_over_text = font.render("GAME OVER! Engine Stalled!", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 20))
        pygame.display.flip()
        time.sleep(3)  # Display the game over screen for 3 seconds
        running = False  # Exit the game loop

pygame.quit()