# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2019 Aiogram
#
# This file is part of ProjectDaisyX.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Build image
FROM python:3.8-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN apt-get install -y --no-install-recommends libyaml-dev

COPY requirements.txt .
RUN pip install --user -r requirements.txt


# Run image
FROM python:3.8-slim AS run-image

# Temp
RUN apt-get update
RUN apt-get install -y --no-install-recommends libyaml-dev

COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

ADD . /DaisyX
RUN rm -rf /DaisyX/data/
WORKDIR /DaisyX

CMD [ "python", "-m", "DaisyX" ]