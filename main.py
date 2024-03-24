import pygame
import sys
import math

# Inicializando o Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW_LIGHT = (255, 255, 204)
BUTTON_ACTIVE_COLOR = (100, 100, 100)

# Definindo constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
RADIUS = 30

# Inicializando a janela
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('JayFlap Simplificado - DFA')

# Lista para armazenar os estados e suas coordenadas
states = []

# Lista para armazenar as transições e seus símbolos
transitions = []

# Lista para armazenar os estados finais
final_states = set()

# Variável para armazenar o estado inicial
initial_state = None

# Definindo a posição da barra de ferramentas
TOOLBAR_HEIGHT = 50

# Definindo cores da barra de ferramentas
TOOLBAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)

# Definindo fonte para os botões
font = pygame.font.SysFont(None, 30)

# Variável para armazenar o texto digitado pelo usuário
input_text = ""

# Função para desenhar a barra de ferramentas
def draw_toolbar():
    pygame.draw.rect(window, TOOLBAR_COLOR, (0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT))

    # Desenhar botão de criar estado
    create_state_button = pygame.Rect(10, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, create_state_button)
    pygame.draw.circle(window, BLACK, (create_state_button.x + 20, create_state_button.y + 15), 10)

    # Desenhar botão de criar transição
    create_transition_button = pygame.Rect(60, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, create_transition_button)
    pygame.draw.line(window, BLACK, (create_transition_button.x + 5, create_transition_button.y + 15),
                     (create_transition_button.x + 35, create_transition_button.y + 15), 3)

    # Desenhar botão de apagar estado ou transição
    delete_button = pygame.Rect(110, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, delete_button)
    draw_text("L", BLACK, delete_button.x + 13, delete_button.y + 5)

    # Botão para definir o estado inicial 
    set_initial_button = pygame.Rect(160, 10, 80, 30)
    pygame.draw.rect(window, BUTTON_COLOR, set_initial_button)
    draw_text("inicial", BLACK, set_initial_button.x + 10, set_initial_button.y + 5)

    # botão estado final 
    set_final_button = pygame.Rect(250, 10, 80, 30)
    pygame.draw.rect(window, BUTTON_COLOR, set_final_button)
    draw_text(" final", BLACK, set_final_button.x + 10, set_final_button.y + 5)

     # Botão para testar palavra
    test_word_button = pygame.Rect(340, 10, 120, 30)
    pygame.draw.rect(window, BUTTON_COLOR, test_word_button)
    draw_text("    Teste", BLACK, test_word_button.x + 10, test_word_button.y + 5)


    return create_state_button, create_transition_button, delete_button, set_initial_button, set_final_button, test_word_button
    
# Função para desenhar os estados
def draw_states():
    for state in states:
        position, name, is_initial = state
        color = YELLOW_LIGHT if not is_initial else (255, 153, 153)  # Vermelho claro para estados iniciais
        if name in final_states:
            border_color = (0, 0, 0)
            pygame.draw.circle(window, border_color, position, RADIUS + 5, 3)  # Desenha uma borda mais grossa para estados finais
        pygame.draw.circle(window, color, position, RADIUS)
        text_surface = font.render(name, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        window.blit(text_surface, text_rect)
        if is_initial:
            draw_initial_arrow(position)

# Função para desenhar os estados iniciais
def draw_initial_arrow(position):
    # Desenhar triângulo apontando para a esquerda
    pygame.draw.polygon(window, BLACK, [(position[0] - RADIUS, position[1]), 
                                         (position[0] - RADIUS - 20, position[1] - 10), 
                                         (position[0] - RADIUS - 20, position[1] + 10)])

# Função para desenhar as transições
def draw_transitions():
    for transition in transitions:
        start_pos = transition[0]
        end_pos = transition[1]
        symbol = transition[2]

        if start_pos != end_pos:  # Se a transição não for um loop
            # Calcular coordenadas médias para o texto
            text_x = (start_pos[0] + end_pos[0]) // 2
            text_y = (start_pos[1] + end_pos[1]) // 2
            
            # Ajustar a posição do texto para cima
            text_y -= 10  # Subtrair 10 pixels para mover o texto para cima
            
            # Exibir o símbolo da transição
            text_surface = font.render(symbol, True, BLACK)
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            window.blit(text_surface, text_rect)
            
            # Desenhar linha entre os estados
            pygame.draw.line(window, BLACK, start_pos, end_pos, 2)
            
            # Desenhar seta direcional
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            angle = math.atan2(dy, dx)
            end_arrow = (end_pos[0] - 15 * math.cos(angle), end_pos[1] - 15 * math.sin(angle))
            pygame.draw.polygon(window, BLACK, ((end_pos[0], end_pos[1]), 
                                                 (end_arrow[0] + 10 * math.sin(angle + 0.4), end_arrow[1] + 10 * math.cos(angle + 0.4)), 
                                                 (end_arrow[0] - 10 * math.sin(angle + 0.4), end_arrow[1] - 10 * math.cos(angle + 0.4))))
        else:  # Se for um loop
            # Calcular a posição final da seta de loop
            end_arrow = (start_pos[0] + RADIUS * math.cos(math.pi / 4), start_pos[1] - RADIUS * math.sin(math.pi / 4))

            # Desenhar a linha curva do loop
            pygame.draw.arc(window, BLACK, (start_pos[0] - RADIUS, start_pos[1] - RADIUS, RADIUS * 2, RADIUS * 2), math.pi / 4, 3 * math.pi / 2, 2)
            
            # Desenhar seta direcional do loop
            dx = end_arrow[0] - start_pos[0]
            dy = end_arrow[1] - start_pos[1]
            angle = math.atan2(dy, dx)
            end_arrow_head = (end_arrow[0] - 10 * math.cos(angle), end_arrow[1] - 10 * math.sin(angle))
            pygame.draw.polygon(window, BLACK, ((end_arrow[0], end_arrow[1]), 
                                                 (end_arrow_head[0] + 5 * math.sin(angle + 0.4), end_arrow_head[1] + 5 * math.cos(angle + 0.4)), 
                                                 (end_arrow_head[0] - 5 * math.sin(angle + 0.4), end_arrow_head[1] - 5 * math.cos(angle + 0.4))))
            
            # Exibir o símbolo da transição no meio do loop
            text_surface = font.render(symbol, True, BLACK)
            text_rect = text_surface.get_rect(center=((start_pos[0] + end_arrow[0]) // 2, (start_pos[1] + end_arrow[1]) // 2))
            window.blit(text_surface, text_rect)

# Função para desenhar texto
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def test_word(word):
    current_state = initial_state
    for symbol in word:
        found_transition = False
        for transition in transitions:
            if transition[0] == current_state and transition[2] == symbol:
                current_state = transition[1]
                found_transition = True
                break
        if not found_transition:
            return False
    return current_state in final_states

# Função principal do programa
def main():
    global states, transitions, input_text, final_states, initial_state, word_test_result

    word_test_result = ""  # Inicializar a variável word_test_result

    running = True
    create_state_active = False
    create_transition_active = False
    delete_active = False
    set_initial_active = False
    set_final_active = False
    start_state = None

    while running:
        window.fill(WHITE)

        create_state_button, create_transition_button, delete_button, set_initial_button, set_final_button, test_word_button = draw_toolbar()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if create_state_button.collidepoint(pos):
                    create_state_active = not create_state_active
                elif create_transition_button.collidepoint(pos):
                    create_transition_active = not create_transition_active
                elif delete_button.collidepoint(pos):
                    delete_active = not delete_active
                elif set_initial_button.collidepoint(pos):
                    set_initial_active = not set_initial_active
                    set_final_active = False
                elif set_final_button.collidepoint(pos):
                    set_final_active = not set_final_active
                    set_initial_active = False
                elif create_state_active:
                    state_name = f'q{len(states)}'  # Nome do estado com prefixo "q" minúsculo e número
                    states.append((pos, state_name, False))
                elif create_transition_active:
                    if start_state is None:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                           RADIUS * 2).collidepoint(pos):
                                start_state = state[0]
                                break
                    else:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                           RADIUS * 2).collidepoint(pos):
                                transitions.append((start_state, state[0], input_text))
                                start_state = None
                                input_text = ""  # Limpar o texto de entrada
                                break
                elif delete_active:
                    for state in states:
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                       RADIUS * 2).collidepoint(pos):
                            states.remove(state)
                            if state[1] in final_states:
                                final_states.remove(state[1])
                            if state[1] == initial_state:
                                initial_state = None
                            break
                    for transition in transitions:
                        if pygame.Rect(transition[0][0], transition[0][1], transition[1][0],
                                       transition[1][1]).collidepoint(pos):
                            transitions.remove(transition)
                            break
                elif set_initial_active:
                    for i, state in enumerate(states):
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                       RADIUS * 2).collidepoint(pos):
                            initial_state = state[1]
                            states[i] = (state[0], state[1], True)
                            break
                elif set_final_active:
                    for state in states:
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                       RADIUS * 2).collidepoint(pos):
                            if state[1] in final_states:
                                final_states.remove(state[1])
                            else:
                                final_states.add(state[1])
                            break
            elif event.type == pygame.KEYDOWN:
                if create_transition_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                           RADIUS * 2).collidepoint(pygame.mouse.get_pos()):
                                transitions.append((start_state, state[0], input_text))
                                start_state = None
                                input_text = ""  # Limpar o texto de entrada
                                break
                    else:
                        input_text += event.unicode

        if create_state_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, create_state_button)
        if create_transition_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, create_transition_button)
            # Desenhar a caixa de entrada de texto para o símbolo da transição
            pygame.draw.rect(window, WHITE, (160, 55, 100, 30))
            pygame.draw.rect(window, BLACK, (160, 55, 100, 30), 2)
            draw_text(input_text, BLACK, 170, 60)

        if delete_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, delete_button)
        if set_initial_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, set_initial_button)
        if set_final_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, set_final_button)

        draw_states()
        draw_transitions()

        # Exibir o resultado do teste da palavra
        draw_text(f"Resultado do teste: {word_test_result}", BLACK, 470, 10)


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
