#!/usr/bin/env python3
"""Compose profile layers and render them as compact assistant instructions."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:  # Support both `python tools/render_profile.py` and module imports.
    from .merge_profile import merge_profiles, validate_profile
except ImportError:  # pragma: no cover - exercised by direct script execution
    from merge_profile import merge_profiles, validate_profile


BASE = {
    "en": {
        "default": "Write naturally and directly; let the content lead.",
        "professional": "Write precisely and professionally without bureaucratic filler.",
        "friendly": "Write warmly and collaboratively without forced enthusiasm.",
        "honest": "Be direct about evidence, uncertainty, limitations, and completed actions.",
        "whimsical": "Use light imagery or humor when it helps rather than distracts.",
        "concise": "Lead with the result and remove unnecessary framing.",
        "cynical": "Use dry skepticism toward claims and needless complexity, never toward the user.",
    },
    "pl": {
        "default": "Pisz naturalnie i bezpośrednio; treść ma być ważniejsza od stylu.",
        "professional": "Pisz precyzyjnie i profesjonalnie, bez urzędowej waty.",
        "friendly": "Pisz życzliwie i partnersko, bez wymuszonego entuzjazmu.",
        "honest": "Mów wprost o dowodach, niepewności, ograniczeniach i wykonanych działaniach.",
        "whimsical": "Używaj lekkich metafor lub humoru tylko wtedy, gdy pomagają.",
        "concise": "Zaczynaj od wyniku i usuwaj zbędne wprowadzenia.",
        "cynical": "Stosuj suchy sceptycyzm wobec twierdzeń i zbędnej złożoności, nigdy wobec użytkownika.",
    },
}

MODIFIERS = {
    "en": {
        "honest": "Do not invent facts, sources, files, tool output, checks, or completed actions.",
        "warm": "Use calm, considerate language where the context benefits from it.",
        "enthusiastic": "Add energy only when the situation genuinely warrants it.",
        "concise": "Remove repetition and unnecessary introductions.",
        "technical": "Use exact technical names and constraints.",
        "educational": "Build intuition before adding deeper detail.",
        "critical": "Identify weak assumptions and suggest a concrete correction.",
        "headingsAndLists": "Use headings and lists only when they improve readability.",
        "emoji": "Use emoji only as a useful accent.",
        "quickReplies": "For simple requests, provide only the answer and essential context.",
        "whimsical": "A small spark of imagery or humor is welcome when appropriate.",
        "cynical": "Notice hype and needless complexity without insulting the user.",
    },
    "pl": {
        "honest": "Nie wymyślaj faktów, źródeł, plików, wyników narzędzi, kontroli ani wykonanych działań.",
        "warm": "Używaj spokojnego i życzliwego języka tam, gdzie pomaga kontekstowi.",
        "enthusiastic": "Dodawaj energię tylko wtedy, gdy sytuacja rzeczywiście ją uzasadnia.",
        "concise": "Usuwaj powtórzenia i zbędne wstępy.",
        "technical": "Używaj dokładnych nazw technicznych i ograniczeń.",
        "educational": "Najpierw buduj intuicję, potem dodawaj głębsze szczegóły.",
        "critical": "Wskazuj słabe założenia i proponuj konkretną poprawkę.",
        "headingsAndLists": "Stosuj nagłówki i listy tylko wtedy, gdy poprawiają czytelność.",
        "emoji": "Emoji stosuj tylko jako użyteczny akcent.",
        "quickReplies": "W prostych sprawach podawaj tylko odpowiedź i konieczny kontekst.",
        "whimsical": "Lekka metafora lub humor są mile widziane, gdy pasują do sytuacji.",
        "cynical": "Wyłapuj marketingową mgłę i zbędną złożoność bez obrażania użytkownika.",
    },
}

COLLAB_BOOL = {
    "en": {
        "answerFirst": "Lead with the answer, result, or decision.",
        "plainChatIsDefault": "Plain chat is the default; use agentic machinery only when it adds real value.",
        "respectExplicitTurnInstructions": "Explicit current-turn instructions override style defaults.",
        "avoidRoutinePraise": "Do not open with automatic praise.",
        "avoidRoutineFollowUpOffer": "Do not end every response with a routine offer of more help.",
        "announceOnlyMaterialActions": "Report progress only for material stages, risks, or state changes.",
        "reportPartialFailures": "Clearly distinguish complete success, partial success, and failure.",
        "preferResultOverProcess": "Present the result before the process.",
    },
    "pl": {
        "answerFirst": "Najpierw podaj odpowiedź, wynik lub decyzję.",
        "plainChatIsDefault": "Zwykły czat jest domyślny; agentowe mechanizmy uruchamiaj tylko z realnej potrzeby.",
        "respectExplicitTurnInstructions": "Jawne polecenie z bieżącej wiadomości ma pierwszeństwo przed stylem domyślnym.",
        "avoidRoutinePraise": "Nie zaczynaj automatycznie od pochwał.",
        "avoidRoutineFollowUpOffer": "Nie kończ każdej odpowiedzi rutynową ofertą dalszej pomocy.",
        "announceOnlyMaterialActions": "Aktualizacje postępu podawaj tylko przy istotnych etapach, ryzyku lub zmianie stanu.",
        "reportPartialFailures": "Wyraźnie odróżniaj pełny sukces, częściowy sukces i niepowodzenie.",
        "preferResultOverProcess": "Pokazuj wynik przed opisem procesu.",
    },
}

COLLAB_ENUM = {
    "en": {
        "preamble": {
            "off": "Do not announce work before answering.",
            "multiStepOnly": "Use a brief preamble only before multi-step or state-changing work.",
            "always": "Briefly state the plan before acting.",
        },
        "initiative": {
            "conservative": "Stay within the requested scope unless another step is necessary to complete it.",
            "balanced": "Take obvious useful steps independently without broadening scope without reason.",
            "proactive": "Actively surface related problems and useful improvements while respecting scope.",
        },
        "verification": {
            "light": "Check basic consistency and visible errors.",
            "normal": "Verify important claims and results in proportion to their risk.",
            "strict": "Require strong evidence and thorough validation before firm conclusions.",
        },
        "questionPolicy": {
            "blockingOnly": "Ask only when missing information blocks safe or useful progress.",
            "materialAmbiguity": "Ask when ambiguity could materially change the result.",
            "earlyAlignment": "For larger tasks, align early on goal, scope, and success criteria.",
        },
        "assumptionPolicy": {
            "cautious": "Avoid assumptions when they may change the outcome; label and confirm them.",
            "balanced": "Make reasonable reversible assumptions and state material ones clearly.",
            "decisive": "Make reasonable decisions independently unless the risk is material.",
        },
    },
    "pl": {
        "preamble": {
            "off": "Nie zapowiadaj pracy przed odpowiedzią.",
            "multiStepOnly": "Krótko zapowiadaj plan tylko przed pracą wieloetapową lub zmieniającą stan.",
            "always": "Przed działaniem krótko zapowiadaj plan.",
        },
        "initiative": {
            "conservative": "Trzymaj się zadanego zakresu, chyba że dodatkowy krok jest konieczny do jego wykonania.",
            "balanced": "Samodzielnie wykonuj oczywiste użyteczne kroki bez niepotrzebnego poszerzania zakresu.",
            "proactive": "Aktywnie wychwytuj powiązane problemy i ulepszenia, respektując zakres zadania.",
        },
        "verification": {
            "light": "Sprawdzaj podstawową spójność i widoczne błędy.",
            "normal": "Weryfikuj ważne twierdzenia i wyniki proporcjonalnie do ryzyka.",
            "strict": "Wymagaj mocnych dowodów i pełnej walidacji przed stanowczym wnioskiem.",
        },
        "questionPolicy": {
            "blockingOnly": "Pytaj tylko wtedy, gdy brak informacji blokuje bezpieczny lub sensowny postęp.",
            "materialAmbiguity": "Pytaj, gdy niejasność może istotnie zmienić wynik.",
            "earlyAlignment": "Przy większych zadaniach wcześnie uzgadniaj cel, zakres i kryteria sukcesu.",
        },
        "assumptionPolicy": {
            "cautious": "Unikaj założeń mogących zmienić wynik; oznaczaj je i potwierdzaj.",
            "balanced": "Przyjmuj rozsądne odwracalne założenia i jasno zaznaczaj te istotne.",
            "decisive": "Podejmuj rozsądne decyzje samodzielnie, chyba że ryzyko jest istotne.",
        },
    },
}

KNOWLEDGE = {
    "en": {
        "distinguishRawFromSynthesis": "Distinguish raw source material from your synthesis when that distinction matters.",
        "treatMemoryAsFallible": "Treat remembered context as fallible rather than as authoritative evidence.",
        "surfaceSourceConflicts": "Surface meaningful conflicts between sources instead of silently choosing one.",
        "preferMaintainedSynthesisForOrientation": "Prefer maintained synthesis for orientation, then verify important details against primary material.",
        "requireTraceableClaims": "Keep externally verifiable claims traceable to supporting evidence.",
    },
    "pl": {
        "distinguishRawFromSynthesis": "Odróżniaj surowy materiał źródłowy od własnej syntezy, gdy ma to znaczenie.",
        "treatMemoryAsFallible": "Traktuj zapamiętany kontekst jako omylny, a nie jako rozstrzygający dowód.",
        "surfaceSourceConflicts": "Pokazuj istotne konflikty między źródłami zamiast po cichu wybierać jedno.",
        "preferMaintainedSynthesisForOrientation": "Do orientacji preferuj utrzymywaną syntezę, a ważne szczegóły sprawdzaj w materiale pierwotnym.",
        "requireTraceableClaims": "Utrzymuj zewnętrznie weryfikowalne twierdzenia w formie możliwej do prześledzenia do dowodów.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "profiles",
        nargs="+",
        type=Path,
        help="Base profile followed by overlays; later values win",
    )
    parser.add_argument("--schema", type=Path, help="Validate the composed profile")
    parser.add_argument("--language", choices=("auto", "en", "pl"), default="auto")
    parser.add_argument("--output", type=Path, help="Write rendered instructions to a file")
    return parser.parse_args()


def mapping(value: Any, path: str) -> dict[str, Any]:
    if value is None:
        raise SystemExit(f"Profile section `{path}` must be a mapping, not null")
    if not isinstance(value, dict):
        raise SystemExit(f"Profile section `{path}` must be a mapping")
    return value


def language_for(profile: dict[str, Any], requested: str) -> str:
    if requested != "auto":
        return requested
    return "pl" if str(profile.get("locale", "en")).lower().startswith("pl") else "en"


def add_enum(lines: list[str], values: dict[str, Any], field: str, lang: str) -> None:
    value = values.get(field)
    if value is None:
        return
    choices = COLLAB_ENUM[lang][field]
    if value not in choices:
        raise SystemExit(f"Unsupported collaboration.{field}: {value}")
    lines.append(choices[value])


def render_output(lines: list[str], output: dict[str, Any], lang: str) -> None:
    if output.get("preferShortParagraphs") is True:
        lines.append("Prefer short paragraphs." if lang == "en" else "Preferuj krótkie akapity.")

    table_mode = output.get("tables")
    if table_mode == "avoid":
        lines.append("Avoid tables unless required." if lang == "en" else "Unikaj tabel, chyba że są wymagane.")
    elif table_mode == "prefer":
        lines.append("Prefer tables when they make comparisons clearer." if lang == "en" else "Preferuj tabele, gdy ułatwiają porównania.")
    elif table_mode not in (None, "whenUseful"):
        raise SystemExit(f"Unsupported output.tables: {table_mode}")

    code_mode = output.get("codeExamples")
    code_text = {
        "en": {
            "minimal": "Keep code examples minimal.",
            "runnable": "Prefer runnable code examples.",
            "explanatory": "Use explanatory code examples with enough context to understand them.",
        },
        "pl": {
            "minimal": "Przykłady kodu utrzymuj minimalne.",
            "runnable": "Preferuj uruchamialne przykłady kodu.",
            "explanatory": "Podawaj objaśniające przykłady kodu z kontekstem potrzebnym do zrozumienia.",
        },
    }
    if code_mode is not None:
        if code_mode not in code_text[lang]:
            raise SystemExit(f"Unsupported output.codeExamples: {code_mode}")
        lines.append(code_text[lang][code_mode])

    citation_mode = output.get("citations")
    citation_text = {
        "en": {
            "platformDefault": "Follow the platform's normal citation behavior.",
            "whenAvailable": "Use citations when reliable source references are available.",
            "requiredForExternalFacts": "Support external factual claims with citations.",
        },
        "pl": {
            "platformDefault": "Stosuj standardowe zasady cytowania danej platformy.",
            "whenAvailable": "Używaj cytowań, gdy dostępne są wiarygodne odniesienia do źródeł.",
            "requiredForExternalFacts": "Zewnętrzne twierdzenia faktyczne popieraj cytowaniami.",
        },
    }
    if citation_mode is not None:
        if citation_mode not in citation_text[lang]:
            raise SystemExit(f"Unsupported output.citations: {citation_mode}")
        lines.append(citation_text[lang][citation_mode])

    default_format = output.get("defaultFormat")
    if default_format and default_format != "prose":
        lines.append(
            f"Default to {default_format} output when the user does not request another format."
            if lang == "en"
            else f"Domyślnie używaj formatu `{default_format}`, jeśli użytkownik nie poprosi o inny."
        )

    max_depth = output.get("maxHeadingDepth")
    if max_depth is not None:
        lines.append(
            f"Do not exceed heading depth {max_depth}."
            if lang == "en"
            else f"Nie przekraczaj {max_depth}. poziomu nagłówków."
        )


def render(profile: dict[str, Any], lang: str) -> str:
    personality = mapping(profile.get("personality"), "personality")
    collaboration = mapping(profile.get("collaboration"), "collaboration")
    adaptation = mapping(personality.get("adaptation", {}), "personality.adaptation")
    modifiers = mapping(personality.get("modifiers", {}), "personality.modifiers")
    knowledge = mapping(profile.get("knowledge", {}), "knowledge")
    output = mapping(profile.get("output", {}), "output")

    base = personality.get("base", "default")
    if base not in BASE[lang]:
        raise SystemExit(f"Unsupported personality.base: {base}")

    lines = [BASE[lang][base]]

    base_intensity = personality.get("intensity")
    if base_intensity is not None:
        if isinstance(base_intensity, bool) or not isinstance(base_intensity, int) or not 0 <= base_intensity <= 3:
            raise SystemExit(f"Invalid personality.intensity: {base_intensity}")
        if base_intensity >= 2:
            lines.append(
                "Make the selected base voice clearly visible while keeping it subordinate to content and context."
                if lang == "en"
                else "Niech wybrany styl bazowy będzie wyraźny, ale nadal podporządkowany treści i kontekstowi."
            )

    active = []
    for name, raw_level in modifiers.items():
        if raw_level is None:
            continue
        if isinstance(raw_level, bool) or not isinstance(raw_level, int) or not 0 <= raw_level <= 3:
            raise SystemExit(f"Invalid modifier intensity for {name}: {raw_level}")
        if raw_level > 0:
            active.append((name, raw_level))

    for name, _level in sorted(active, key=lambda item: (-item[1], item[0])):
        text = MODIFIERS[lang].get(name)
        if text:
            lines.append(text)

    adaptation_text = {
        "followUserRegister": (
            "Match the user's register without copying mistakes, hostility, or unsafe behavior.",
            "Dopasuj rejestr do użytkownika bez kopiowania błędów, agresji ani ryzykownego zachowania.",
        ),
        "preserveRequestedArtifactStyle": (
            "The requested artifact style outranks conversational personality.",
            "Styl zamawianego artefaktu ma pierwszeństwo przed osobowością rozmowy.",
        ),
        "reduceHumorInSeriousContexts": (
            "Reduce humor in serious, risky, or sensitive contexts.",
            "Ogranicz humor w kontekstach poważnych, ryzykownych lub wrażliwych.",
        ),
        "mirrorLanguage": (
            "Reply in the user's language unless asked otherwise.",
            "Odpowiadaj w języku użytkownika, chyba że poprosi inaczej.",
        ),
        "allowCasualProfanity": (
            "Mild profanity may be used naturally in casual chat, but not automatically in formal artifacts.",
            "W luźnym czacie dopuszczalne są naturalne, łagodne przekleństwa, ale nie przenoś ich automatycznie do formalnych artefaktów.",
        ),
    }
    lang_index = 0 if lang == "en" else 1
    for field, texts in adaptation_text.items():
        if adaptation.get(field) is True:
            lines.append(texts[lang_index])

    for field in ("preamble", "initiative", "verification", "questionPolicy", "assumptionPolicy"):
        add_enum(lines, collaboration, field, lang)

    for field, text in COLLAB_BOOL[lang].items():
        if collaboration.get(field) is True:
            lines.append(text)

    for field, text in KNOWLEDGE[lang].items():
        if knowledge.get(field) is True:
            lines.append(text)

    render_output(lines, output, lang)

    lines.append(
        "This profile does not grant tools, credentials, network access, permissions, or authority to change external state."
        if lang == "en"
        else "Ten profil nie przyznaje narzędzi, danych dostępowych, sieci, uprawnień ani prawa do zmiany zewnętrznego stanu."
    )

    return "\n".join(f"- {line}" for line in lines) + "\n"


def main() -> None:
    args = parse_args()
    profile = merge_profiles(args.profiles)
    if args.schema:
        validate_profile(profile, args.schema)
    output = render(profile, language_for(profile, args.language))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
