from pytestarch import Rule, EvaluableArchitecture


def test_shared_kernel_should_not_depend_on_business_modules(
    get_evaluable_architecture: EvaluableArchitecture,
) -> None:
    """Shared kernel independence test."""
    all_modules = [m for m in get_evaluable_architecture.modules]

    # Check if business modules exist
    has_modules_folder = any(".modules." in m for m in all_modules)

    if not has_modules_folder:
        return  # No business modules yet, test passes

    rule = (
        Rule()
        .modules_that()
        .have_name_matching(r".*shared_kernel.*")
        .should_not()
        .import_modules_that()
        .have_name_matching(r".*\.modules\..*")
    )

    rule.assert_applies(get_evaluable_architecture)


def test_domain_should_not_depend_on_application_or_infrastructure(
    get_evaluable_architecture: EvaluableArchitecture,
) -> None:
    """Domain layer must be pure - no dependencies on other layers."""
    rule = (
        Rule()
        .modules_that()
        .have_name_matching(r".*shared_kernel\.domain.*")
        .should_not()
        .import_modules_that()
        .have_name_matching(r".*shared_kernel\.(application|infrastructure).*")
    )
    rule.assert_applies(get_evaluable_architecture)


def test_application_should_not_depend_on_infrastructure(
    get_evaluable_architecture: EvaluableArchitecture,
) -> None:
    """Application layer should only depend on domain (ports & adapters)."""
    rule = (
        Rule()
        .modules_that()
        .have_name_matching(r".*shared_kernel\.application.*")
        .should_not()
        .import_modules_that()
        .have_name_matching(r".*shared_kernel\.infrastructure.*")
    )
    rule.assert_applies(get_evaluable_architecture)
