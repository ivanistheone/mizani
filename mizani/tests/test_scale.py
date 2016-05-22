from __future__ import division

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest

from ..bounds import rescale
from ..scale import scale_continuous, scale_discrete
from ..transforms import identity_trans


def test_scale_continuous():
    x = np.arange(11)
    # apply
    scaled = scale_continuous.apply(x, rescale)
    npt.assert_allclose(scaled, x*0.1)
    npt.assert_allclose(scaled, x*0.1)

    # Train
    limits = scale_continuous.train(x)
    npt.assert_allclose(limits, [0, 10])
    # Additional training
    limits = scale_continuous.train(np.arange(-4, 11), limits)
    npt.assert_allclose(limits, [-4, 10])
    limits = scale_continuous.train([], limits)
    npt.assert_allclose(limits, [-4, 10])

    # branches #
    scaled = scale_continuous.apply(x, rescale,
                                    trans=identity_trans())
    mapped = scale_continuous.map(x, list, [0, 10])
    npt.assert_allclose(mapped, x*0.1)

    with pytest.raises(TypeError):
        # discrete data
        limits = scale_continuous.train(['a', 'b', 'c'])


def test_scale_discrete():
    x = ['a', 'b', 'c', 'a']
    # apply
    scaled = scale_discrete.apply(x, np.arange)
    npt.assert_allclose(scaled, [0, 1, 2, 0])

    # Train
    limits = scale_discrete.train(x)
    assert limits == ['a', 'b', 'c']

    # Additional training
    limits = scale_discrete.train(['b', 'c', 'd'], limits)
    assert limits == ['a', 'b', 'c', 'd']
    limits = scale_discrete.train([], limits)
    assert limits == ['a', 'b', 'c', 'd']

    # branches #

    with pytest.raises(TypeError):
        # continuous data
        limits = scale_discrete.train([1, 2, 3])

    x = pd.Categorical(['a', 'b'])
    limits = scale_discrete.train(x)
    assert limits == ['a', 'b']

    x = pd.Series(['a', 'b', 'c'], dtype='category')
    limits = scale_discrete.train(x[:1], drop=True)
    assert limits == ['a']

    limits = scale_discrete.train(x[:2], drop=False)
    assert limits == ['a', 'b', 'c']
