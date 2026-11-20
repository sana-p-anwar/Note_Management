from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from notes_app.serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from notes_app.serializers import NotesSerializer,TaskSerializer
from notes_app.models import NotesDb,TaskDb
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def post(self,request):
        serializer_instance = RegisterSerializer(data = request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data = {
                "Message":"registration succesfull"
            })
        else:
            return Response(data = serializer_instance.errors)
        
class NotesListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes,many=True)
        return Response(serializer_instance.data)
    def post(self, request):
        serializer_instance = NotesSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)

            return Response(data={
                "Message": "Note created successfully",
                "Data": serializer_instance.data
            })

        else:
            return Response(data=serializer_instance.errors)
        
class NotesRetrieveUpdateDeleteView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk, user=request.user)
        except NotesDb.DoesNotExist:
            return Response(data={"Message": "Note not found"})

        serializer_instance = NotesSerializer(note)

        return Response(serializer_instance.data)

    def put(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk, user=request.user)
        except NotesDb.DoesNotExist:
            return Response(data={"Message": "Note not found"})

        serializer_instance = NotesSerializer(note, data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)

            return Response(data={
                "Message": "Note updated successfully",
                "Data": serializer_instance.data
            })

        return Response(data=serializer_instance.errors)

    def delete(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk, user=request.user)
        except NotesDb.DoesNotExist:
            return Response(data={"Message": "Note not found"})

        note.delete()

        return Response(data={
            "Message": "Note deleted successfully"
        })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message":"Logout Success"
        })
    
class TaskListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    # READ ALL TASKS
    def get(self, request):

        tasks = TaskDb.objects.filter(user=request.user)

        serializer_instance = TaskSerializer(tasks, many=True)

        return Response(serializer_instance.data)


    # CREATE TASK
    def post(self, request):

        serializer_instance = TaskSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(user=request.user)

            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)
    
class TaskRetrieveUpdateDeleteView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_task(self, request, id):
        return get_object_or_404(
            TaskDb,
            id=id,
            user=request.user
        )
    def get(self, request, id):
        task = self.get_task(request, id)
        serializer_instance = TaskSerializer(task)
        return Response(serializer_instance.data)
    def put(self, request, id):
        task = self.get_task(request, id)

        form_data = request.data

        serializer_instance = TaskSerializer(data=form_data, instance=task)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)

        return Response(serializer_instance.errors)
    
    # DELETE TASK
    def delete(self, request, id):
        task = self.get_task(request, id)

        task.delete()

        return Response(
        {
            "Message": "Task deleted successfully..!"
        }
    )
    
