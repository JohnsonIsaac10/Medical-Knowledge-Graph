from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
import json
from app01.KG_code.main_func import main_handler


def index(request):
    return render(request, 'entity_search.html')


def entity_search(request):
    ctx = {}

    if (request.GET):
        entity = request.GET['user_text']
        entity = entity.strip()
        entity = entity.lower()
        entity = ''.join(entity.split())

        entityRelation = main_handler.search_entity_main(entity)
        print(entity)
        if len(entityRelation) == 0:
            ctx = {'title': '<h2>知识库中暂未添加该实体</h1>'}
            return render(request, 'entity_search.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
        else:
            return render(request, 'entity_search.html',
                          {'entityRelation': json.dumps(entityRelation, ensure_ascii=False)})

    return render(request, 'entity_search.html', ctx)


def search_knowledge(request):
    ctx = {}
    if (request.GET):
        question = request.GET['question']
        question = question.strip()
        question = question.lower()
        answer = main_handler.chat_main(question)
        final_answer = {'final_answer': answer}
        return render(request, 'search_knowledge.html', {'ret': final_answer})

    return render(request, 'search_knowledge.html', ctx)


def question_answering(request):
    ctx = {}
    if (request.GET):
        question = request.GET['question']
        question = question.strip()
        question = question.lower()
        answer = main_handler.chat_main(question)
        final_answer = {'final_answer': answer}
        return JsonResponse({'ret': final_answer})

    return render(request, 'question_answering.html', ctx)