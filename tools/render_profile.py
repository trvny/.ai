#!/usr/bin/env python3
"""Compose profile layers and render them as compact assistant instructions."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

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

COLLAB = {
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


def language_for(profile: dict[str, Any], requested: str) -> str:
    if requested != "auto":
        return requested
    return "pl" if str(profile.get("locale", "en")).lower().startswith("pl") else "en"


def render(profile: dict[str, Any], lang: str) -> str:
    personality = profile.get("personality", {})
    collaboration = profile.get("collaboration", {})
    adaptation = personality.get("adaptation", {})
    modifiers = personality.get("modifiers", {})

    base = personality.get("base", "default")
    if base not in BASE[lang]:
        raise SystemExit(f"Unsupported personality.base: {base}")

    lines = [BASE[lang][base]]

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

    if adaptation.get("followUserRegister", True):
        lines.append(
            "Match the user's register without copying mistakes, hostility, or unsafe behavior."
            if lang == "en"
            else "Dopasuj rejestr do użytkownika bez kopiowania błędów, agresji ani ryzykownego zachowania."
        )
    if adaptation.get("preserveRequestedArtifactStyle", True):
        lines.append(
            "The requested artifact style outranks conversational personality."
            if lang == "en"
            else "Styl zamawianego artefaktu ma pierwszeństwo przed osobowością rozmowy."
        )
    if adaptation.get("reduceHumorInSeriousContexts", True):
        lines.append(
            "Reduce humor in serious, risky, or sensitive contexts."
            if lang == "en"
            else "Ogranicz humor w kontekstach poważnych, ryzykownych lub wrażliwych."
        )
    if adaptation.get("mirrorLanguage", True):
        lines.append(
            "Reply in the user's language unless asked otherwise."
            if lang == "en"
            else "Odpowiadaj w języku użytkownika, chyba że poprosi inaczej."
        )
    if adaptation.get("allowCasualProfanity", False):
        lines.append(
            "Mild profanity may be used naturally in casual chat, but not automatically in formal artifacts."
            if lang == "en"
            else "W luźnym czacie dopuszczalne są naturalne, łagodne przekleństwa, ale nie przenoś ich automatycznie do formalnych artefaktów."
        )

    preamble = collaboration.get("preamble", "multiStepOnly")
    preamble_text = {
        "en": {
            "off": "Do not announce work before answering.",
            "multiStepOnly": "Use a brief preamble only before multi-step or state-changing work.",
            "always": "Briefly state the plan before acting.",
        },
        "pl": {
            "off": "Nie zapowiadaj pracy przed odpowiedzią.",
            "multiStepOnly": "Krótko zapowiadaj plan tylko przed pracą wieloetapową lub zmieniającą stan.",
            "always": "Przed działaniem krótko zapowiadaj plan.",
        },
    }
    if preamble not in preamble_text[lang]:
        raise SystemExit(f"Unsupported collaboration.preamble: {preamble}")
    lines.append(preamble_text[lang][preamble])

    for field, text in COLLAB[lang].items():
        if collaboration.get(field, True):
            lines.append(text)

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
