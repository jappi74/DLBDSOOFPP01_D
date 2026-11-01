from repository import JsonRepository
from controller import DashboardController
from view import DashboardView

def main():
    repo = JsonRepository()
    student = repo.lade_daten()
    controller = DashboardController(student)
    view = DashboardView(controller)
    view.render()

if __name__ == "__main__":
    main()