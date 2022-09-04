FROM node:slim

WORKDIR /usr/src/mockpass

RUN npm install @opengovsg/mockpass

ENV SHOW_LOGIN_PAGE=true

CMD ["npx", "mockpass"]
