# -*- coding: utf-8 -*-
"""
Unit tests from mathics.builtin.attributes.
"""

import os
from test.helper import check_evaluation, session

import pytest

DEBUGRULESPAT = int(os.environ.get("DEBUGRULESPAT", "0")) == 1

if DEBUGRULESPAT:
    skip_or_fail = pytest.mark.xfail
else:
    skip_or_fail = pytest.mark.skip


@pytest.mark.parametrize(
    ("str_expr", "str_expected", "msg"),
    [
        (None, None, None),
        # F has the attribute, but G doesn't.
        ("SetAttributes[F, OneIdentity]", "Null", None),
        ("SetAttributes[r, Flat]", "Null", None),
        ("SetAttributes[s, Flat]", "Null", None),
        ("SetAttributes[s, OneIdentity]", "Null", None),
        ("MatchQ[x, F[y_]]", "False", "With OneIdentity"),
        ("MatchQ[x, G[y_]]", "False", "Without OneIdentity"),
        ("MatchQ[x, F[x_:0,y_]]", "True", "With OneIdentity, and Default"),
        ("MatchQ[x, G[x_:0,y_]]", "False", "Without OneIdentity, and Default"),
        ("MatchQ[F[x], F[x_:0,y_]]", "True", "With OneIdentity, and Default"),
        ("MatchQ[G[x], G[x_:0,y_]]", "True", "Without OneIdentity, and Default"),
        ("MatchQ[F[F[F[x]]], F[x_:0,y_]]", "True", "With OneIdentity, nested"),
        ("MatchQ[G[G[G[x]]], G[x_:0,y_]]", "True", "Without OneIdentity, nested"),
        ("MatchQ[F[3, F[F[x]]], F[x_:0,y_]]", "True", "With OneIdentity, nested"),
        ("MatchQ[G[3, G[G[x]]], G[x_:0,y_]]", "True", "Without OneIdentity, nested"),
        (
            "MatchQ[x, F[x1_:0, F[x2_:0,y_]]]",
            "True",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, G[x1_:0, G[x2_:0,y_]]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, F[x1___:0, F[x2_:0,y_]]]",
            "True",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, G[x1___:0, G[x2_:0,y_]]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        ("MatchQ[x, F[F[x2_:0,y_],x1_:0]]", "True", "With OneIdentity, pattern nested"),
        (
            "MatchQ[x, G[G[x2_:0,y_],x1_:0]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        ("MatchQ[x, F[x_.,y_]]", "False", "With OneIdentity, and Optional, no default"),
        (
            "MatchQ[x, G[x_.,y_]]",
            "False",
            "Without OneIdentity, and Optional, no default",
        ),
        ("Default[F, 1]=1.", "1.", None),
        ("Default[G, 1]=2.", "2.", None),
        ("MatchQ[x, F[x_.,y_]]", "True", "With OneIdentity, and Optional, default"),
        ("MatchQ[x, G[x_.,y_]]", "False", "Without OneIdentity, and Optional, default"),
        ("MatchQ[F[F[H[y]]],F[x_:0,u_H]]", "False", None),
        ("MatchQ[G[G[H[y]]],G[x_:0,u_H]]", "False", None),
        ("MatchQ[F[p, F[p, H[y]]],F[x_:0,u_H]]", "False", None),
        ("MatchQ[G[p, G[p, H[y]]],G[x_:0,u_H]]", "False", None),
        (None, None, None),
    ],
)
def test_one_identity(str_expr, str_expected, msg):
    check_evaluation(
        str_expr,
        str_expected,
        to_string_expr=True,
        to_string_expected=True,
        hold_expected=True,
        failure_message=msg,
    )


@pytest.mark.parametrize(
    ("str_expr", "str_expected", "msg"),
    [
        (None, None, None),
        # F has the attribute, but G doesn't.
        ("SetAttributes[F, OneIdentity]", "Null", None),
        ("SetAttributes[r, Flat]", "Null", None),
        ("SetAttributes[s, Flat]", "Null", None),
        ("SetAttributes[s, OneIdentity]", "Null", None),
        # Replace also takes into account the OneIdentity attribute,
        # and also modifies the interpretation of the Flat attribute.
        (
            "F[a,b,b,c]/.F[x_,x_]->Fp[x]",
            "F[a, b, b, c]",
            "https://reference.wolfram.com/language/tutorial/Patterns.html",
        ),
        # When fixed, Add the difference between the next two as a
        # doctest example.
        (
            "r[a,b,b,c]/.r[x_,x_]->rp[x]",
            "r[a, rp[r[b]], c]",
            "https://reference.wolfram.com/language/tutorial/Patterns.html",
        ),
        (
            "s[a,b,b,c]/.s[x_,x_]->sp[x]",
            "s[a, rp[b], c]",
            "https://reference.wolfram.com/language/tutorial/Patterns.html",
        ),
        (None, None, None),
    ],
)
@skip_or_fail
def test_one_identity_still_failing(str_expr, str_expected, msg):
    check_evaluation(
        str_expr,
        str_expected,
        to_string_expr=True,
        to_string_expected=True,
        hold_expected=True,
        failure_message=msg,
    )


@pytest.mark.parametrize(
    ("str_expr", "str_expected", "msg"),
    [
        (None, None, None),
        # F has the attribute, but G doesn't.
        ("SetAttributes[F, OneIdentity]", "Null", None),
        ("SetAttributes[r, Flat]", "Null", None),
        ("SetAttributes[s, Flat]", "Null", None),
        ("SetAttributes[s, OneIdentity]", "Null", None),
        ("MatchQ[x, F[y_]]", "False", "With OneIdentity"),
        ("MatchQ[x, G[y_]]", "False", "Without OneIdentity"),
        ("MatchQ[x, F[x_:0,y_]]", "True", "With OneIdentity, and Default"),
        ("MatchQ[x, G[x_:0,y_]]", "False", "Without OneIdentity, and Default"),
        ("MatchQ[F[x], F[x_:0,y_]]", "True", "With OneIdentity, and Default"),
        ("MatchQ[G[x], G[x_:0,y_]]", "True", "Without OneIdentity, and Default"),
        ("MatchQ[F[F[F[x]]], F[x_:0,y_]]", "True", "With OneIdentity, nested"),
        ("MatchQ[G[G[G[x]]], G[x_:0,y_]]", "True", "Without OneIdentity, nested"),
        ("MatchQ[F[3, F[F[x]]], F[x_:0,y_]]", "True", "With OneIdentity, nested"),
        ("MatchQ[G[3, G[G[x]]], G[x_:0,y_]]", "True", "Without OneIdentity, nested"),
        (
            "MatchQ[x, F[x1_:0, F[x2_:0,y_]]]",
            "True",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, G[x1_:0, G[x2_:0,y_]]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, F[x1___:0, F[x2_:0,y_]]]",
            "True",
            "With OneIdentity, pattern nested",
        ),
        (
            "MatchQ[x, G[x1___:0, G[x2_:0,y_]]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        ("MatchQ[x, F[F[x2_:0,y_],x1_:0]]", "True", "With OneIdentity, pattern nested"),
        (
            "MatchQ[x, G[G[x2_:0,y_],x1_:0]]",
            "False",
            "With OneIdentity, pattern nested",
        ),
        ("MatchQ[x, F[x_.,y_]]", "False", "With OneIdentity, and Optional, no default"),
        (
            "MatchQ[x, G[x_.,y_]]",
            "False",
            "Without OneIdentity, and Optional, no default",
        ),
        ("Default[F, 1]=1.", "1.", None),
        ("Default[G, 1]=2.", "2.", None),
        ("MatchQ[x, F[x_.,y_]]", "True", "With OneIdentity, and Optional, default"),
        ("MatchQ[x, G[x_.,y_]]", "False", "Without OneIdentity, and Optional, default"),
        ("MatchQ[F[F[H[y]]],F[x_:0,u_H]]", "False", None),
        ("MatchQ[G[G[H[y]]],G[x_:0,u_H]]", "False", None),
        ("MatchQ[F[p, F[p, H[y]]],F[x_:0,u_H]]", "False", None),
        ("MatchQ[G[p, G[p, H[y]]],G[x_:0,u_H]]", "False", None),
        (None, None, None),
    ],
)
@skip_or_fail
def test_one_identity_stil_failing(str_expr, str_expected, msg):
    check_evaluation(
        str_expr,
        str_expected,
        to_string_expr=True,
        to_string_expected=True,
        hold_expected=True,
        failure_message=msg,
    )


@pytest.mark.parametrize(
    ("str_expr", "arg_count"),
    [
        ("SetAttributes[F]", 1),
        ("SetAttributes[]", 0),
        ("SetAttributes[F, F, F]", 3),
    ],
)
def test_Attributes_wrong_args(str_expr, arg_count):
    check_evaluation(
        str_expr=str_expr,
        str_expected=str_expr,
        failure_message=f"Arg count mismatch test with {arg_count} args",
        hold_expected=True,
        to_string_expr=True,
        to_string_expected=True,
        expected_messages=(
            f"SetAttributes called with {arg_count} arguments; 2 arguments are expected.",
        ),
    )


@pytest.mark.parametrize(
    ("str_expr", "msgs", "str_expected", "fail_msg"),
    [
        ("CleanAll[u];CleanAll[v];", None, None, None),
        ("SetAttributes[{u, v}, Flat];u[x_] := {x};u[]", None, "u[]", None),
        ("u[a]", None, "{a}", None),
        ("v[x_] := x;v[]", None, "v[]", None),
        ("v[a]", None, "a", None),
        (
            "v[a, b]",
            None,
            "v[a, b]",
            "in Mathematica: Iteration limit of 4096 exceeded.",
        ),
        ("CleanAll[u];CleanAll[v];", None, None, None),
    ],
)
def test_private_doctests_attributes(str_expr, msgs, str_expected, fail_msg):
    """ """
    check_evaluation(
        str_expr,
        str_expected,
        to_string_expr=True,
        to_string_expected=True,
        hold_expected=True,
        failure_message=fail_msg,
        expected_messages=msgs,
    )


@pytest.mark.parametrize(
    ("str_expr", "msgs", "str_expected", "fail_msg"),
    [
        ("CleanAll[u];CleanAll[v];", None, None, None),
        (
            "SetAttributes[{u, v}, Flat];u[x_] := {x};u[a, b]",
            ("Iteration limit of 1000 exceeded.",),
            "$Aborted",
            None,
        ),
        ("u[a, b, c]", ("Iteration limit of 1000 exceeded.",), "$Aborted", None),
        (
            "v[x_] := x;v[a,b,c]",
            ("Iteration limit of 1000 exceeded.",),
            "$Aborted",
            "in Mathematica: Iteration limit of 4096 exceeded.",
        ),
        ("CleanAll[u];CleanAll[v];", None, None, None),
    ],
)
def test_private_doctests_attributes_with_exceptions(
    str_expr, msgs, str_expected, fail_msg
):
    """These tests check the behavior of $RecursionLimit and $IterationLimit"""

    # Here we do not use the session object to check the messages
    # produced by the exceptions. If $RecursionLimit / $IterationLimit
    # are reached during the evaluation using a MathicsSession object,
    # an exception is raised. On the other hand, using the `Evaluation.evaluate`
    # method, the exception is handled.
    #
    # TODO: Maybe it makes sense to clone this exception handling in
    # the check_evaluation function.
    #
    def eval_expr(expr_str):
        query = session.evaluation.parse(expr_str)
        res = session.evaluation.evaluate(query)
        session.evaluation.stopped = False
        return res

    res = eval_expr(str_expr)
    if msgs is None:
        assert len(res.out) == 0
    else:
        assert len(res.out) == len(msgs)
        for li1, li2 in zip(res.out, msgs):
            assert li1.text == li2

    assert res.result == str_expected
